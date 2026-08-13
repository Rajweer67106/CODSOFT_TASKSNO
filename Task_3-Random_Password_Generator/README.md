# Task 3 — Random Password Generator

This project is part of my Artificial Intelligence Internship and Python Programming Track.

It is a desktop password generator that creates strong passwords according to the user's selected requirements. The project also demonstrates secure random generation, GUI development, clipboard integration, validation, and session history.

## Features

- Password length from 8 to 64 characters
- Uppercase letters
- Lowercase letters
- Numbers
- Symbols
- Minimum 2 character types required
- Guarantees at least one character from every selected type
- Uses Python's `secrets` module for security-sensitive generation
- Password strength indicator
- Copy to clipboard
- Exclude ambiguous characters such as O, 0, I, l, 1 and |
- Generate another password without restarting
- Last 5 generated passwords shown during the current session
- No password history is saved to disk

## Technologies Used

- Python
- Tkinter
- secrets
- string
- pyperclip

## Installation

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## How to Use

1. Select the password length.
2. Select at least two character types.
3. Optionally enable ambiguous-character exclusion.
4. Click **Generate Password**.
5. Check the strength indicator.
6. Click **Copy to Clipboard** if required.
7. Use **Generate Another** to create another password.

## Security

The application uses Python's `secrets` module rather than `random` because `secrets` is intended for generating unpredictable values for security-sensitive applications.

Password history is kept only in memory during the current session and is not stored in a file or database.

## Project Structure

```text
Task_3-Random_Password_Generator/
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```
