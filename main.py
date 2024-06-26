import requests
import json
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import ConnectionError, Timeout
from tqdm import tqdm


def generate_semester_ids(start_year, end_year):
    semesters = {}
    for year in range(start_year, end_year + 1):
        year_short = str(year)[-2:]
        semesters[f"{year_short}1"] = f"Spring {year}"
        semesters[f"{year_short}2"] = f"Summer {year}"
        semesters[f"{year_short}3"] = f"Fall {year}"
    return semesters


def get_semester_choice(semesters):
    print("Select a semester ID:")
    for sem_id, description in semesters.items():
        print(f"{sem_id} - {description}")

    while True:
        selected_id = input("Enter the semester ID: ")
        if selected_id in semesters:
            return selected_id
        else:
            print("Invalid semester ID. Please try again.")


def fetch_data(url):
    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except (ConnectionError, Timeout) as e:
            print(f"Attempt {i + 1} failed: {e}")
            sleep(2)
    return None


def fetch_student_info(id):
    student_info_api = (
        f"http://software.diu.edu.bd:8006/result/studentInfo?studentId={id}"
    )
    student_info_response = fetch_data(student_info_api)

    if student_info_response:
        try:
            student_info_dic = json.loads(student_info_response.text)
            student_name = student_info_dic.get("studentName")
            return student_name, id
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for student info of ID {id}")
            return None, id
    else:
        print(f"Failed to fetch student info for ID {id}")
        return None, id


def fetch_student_results(student_name, id, semester_id):
    result_api = f"http://software.diu.edu.bd:8006/result?grecaptcha=&semesterId={semester_id}&studentId={id}"
    result_response = fetch_data(result_api)

    if result_response:
        try:
            result_dic = json.loads(result_response.text)
            if result_dic:
                cgpa = result_dic[0].get("cgpa")
                return student_name, id, cgpa
            else:
                print(f"No result found for {student_name} ({id})")
                return student_name, id, None
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for {student_name} ({id})")
            return student_name, id, None
    else:
        print(f"Failed to fetch result for {student_name} ({id})")
        return student_name, id, None


def main():
    file_path = "section-ids.txt"
    with open(file_path, "r") as file:
        ids = [line.strip() for line in file.readlines()]

    semesters = generate_semester_ids(2010, 2030)
    semester_id = get_semester_choice(semesters)

    results = []

    with tqdm(total=len(ids), desc="Fetching student data") as pbar:
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_student_info = {
                executor.submit(fetch_student_info, id): id for id in ids
            }
            for future in as_completed(future_to_student_info):
                student_name, id = future.result()
                if student_name:
                    future_to_result = executor.submit(
                        fetch_student_results, student_name, id, semester_id
                    )
                    results.append(future_to_result)
                pbar.update(1)

    results = [future.result() for future in results]

    results = [result for result in results if result[2] is not None]

    sorted_results = sorted(results, key=lambda x: x[2], reverse=True)

    top_10 = sorted_results[:10]
    other_students = sorted_results[10:]

    print("\nTop 10 Students:")
    for index, result in enumerate(top_10, start=1):
        student_name, student_id, cgpa = result
        print(f"{index}. {student_name} ({student_id}): {cgpa}")

    print("\nOther Students:")
    for index, result in enumerate(other_students, start=11):
        student_name, student_id, cgpa = result
        print(f"{index}. {student_name} ({student_id}): {cgpa}")


if __name__ == "__main__":
    main()
