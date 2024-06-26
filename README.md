# DIU Academic Leaderboard

This project fetches and displays academic performance data for students from Daffodil International University (DIU). It retrieves and ranks students based on their CGPA for a specific semester chosen by the user.

## Features

- Fetches student data from DIU's academic result API.
- Allows selection of semester IDs spanning from 2010 to 2030.
- Displays the top-performing students based on CGPA.
- Handles errors gracefully when fetching data.

## Requirements

- Python 3.x
- `requests` library
- `tqdm` library (for progress bar)

## Installation

Clone the repository:

```bash
git clone https://github.com/wsjishan/diu-academic-leaderboard.git
cd diu-academic-leaderboard
```

Ensure requests library is installed:

```bash
pip install requests
```

If you prefer to use the progress bar during data fetching, ensure tqdm is installed:

```bash
pip install tqdm
```

## Add Student IDs to section-ids.txt File:

Create a text file named section-ids.txt in the project directory. Each line in this file should contain a student ID.

Example section-ids.txt:

- 222-15-6163
- 222-15-6299
- 222-15-6242
- Add more student IDs as needed, one per line

### **Run the Script:**

```bash
python check_follow_back.py
```

## Submit Your Section IDs

To contribute to the DIU Academic Leaderboard project by submitting your section IDs, please fill out the [Section IDs Submission Form.](https://forms.gle/Zw22xVY96Y3e1EDS9)

Your participation helps improve and expand the dataset used in this project. Thank you for your contribution!
