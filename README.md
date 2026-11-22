# Library Management System

A Python 3 console application based on the supplied Library Management System PRD.

## Features
- List all books.
- Search by ISBN or keyword (title, author, or genre).
- Borrow and return books.
- View the current local member's borrowing history.
- Track due dates and identify overdue loans.
- Store books, members, and loans in a local JSON file.
- Validate inputs and handle file/data errors.

## Project structure

```text
project-root/
├── src/
│   ├── main.py
│   ├── book.py
│   ├── member.py
│   ├── loan.py
│   ├── library.py
│   ├── storage.py
│   └── data.json
├── tests/
│   └── test_library.py
└── README.md
```

## Requirements
- Python 3.8 or later
- No third-party packages required

## Run
From the project root:

```bash
python src/main.py
```

The program creates/updates `src/data.json` automatically. To add the initial collection,
edit `src/data.json` and add book objects to the `books` list, for example:

```json
{
  "books": [
    {
      "title": "The Hobbit",
      "author": "J.R.R. Tolkien",
      "genre": "Fantasy",
      "isbn": "9780547928227"
    }
  ],
  "members": [],
  "loans": []
}
```

On the first borrowing attempt, the application asks for the local member's name and email.
The PRD describes a single local user and does not specify a separate member-registration
menu, so the profile is created during the first borrow operation.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Notes about implementation choices
- The PRD does not state a loan duration. This implementation uses a 14-day default,
  defined by `Library.LOAN_PERIOD_DAYS` in `src/library.py`; change it if your instructor
  specifies another duration.
- The PRD's menu/API table specifies ISBN input for borrowing and returning. The app uses
  ISBN for both operations.
- The PRD specifies JSON persistence, lists of `Book`, `Member`, and `Loan` records,
  no duplicate ISBNs, and required non-empty fields.
