# BMI Calculator — Advanced GUI Version

A Python Tkinter BMI Calculator built for the Python Programming Track (Task 2).

## Features

- GUI application using Tkinter
- User name, weight (kg), and height (m) input
- BMI calculation using:

  `BMI = weight / height²`

- BMI classification:
  - Underweight: BMI < 18.5
  - Normal: 18.5–24.9
  - Overweight: 25–29.9
  - Obese: BMI ≥ 30
- BMI rounded to 2 decimal places
- Colour-coded result feedback
- Multi-user support
- Historical records stored in SQLite
- Saved BMI history displayed in the application
- BMI trend graph using Matplotlib
- Input validation and helpful error messages
- Database error handling

## Requirements

- Python 3.9 or newer recommended
- Tkinter
- Matplotlib

Tkinter is included with most Windows Python installations. On some Linux distributions, install the OS package separately (for example, `python3-tk`).

## Installation

Open a terminal/command prompt in this project folder.

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The SQLite database file `bmi_history.db` is automatically created the first time the program runs.

## How to use

1. Enter a user name.
2. Enter weight in kilograms.
3. Enter height in metres.
4. Click **Calculate & Save**.
5. The BMI and category appear with colour-coded feedback.
6. Saved records appear in the history table.
7. Enter/select a user and click **Show BMI Trend** to display the user's BMI graph.
8. Double-clicking a history row selects that user.

## Project structure

```text
BMI_Calculator_Advanced/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The file `bmi_history.db` is generated automatically at runtime and is intentionally ignored by Git.

## Viva / Project Explanation

### Formula
BMI is calculated as:

```text
BMI = weight (kg) / height (m)²
```

### Why SQLite?
SQLite provides persistent local storage without requiring a separate database server. Each calculation is stored with the user name, weight, height, BMI, category, and timestamp.

### Why Matplotlib?
Matplotlib is used to visualize a user's BMI history as a line chart, making changes over time easy to understand.

### Input validation
The application rejects:
- Empty user names
- Non-numeric weight/height
- Zero or negative values
- Clearly invalid extreme values
- Height values above 3 metres

### Technologies
- Python
- Tkinter / ttk
- SQLite3
- Matplotlib
- datetime
