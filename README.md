# Library Book Management System --- Group 32

**DevOps Experiment:** Design and execute a Continuous Integration (CI)
workflow using GitHub Actions to automatically build/check and test an
application.

A college-library web application built with **Python, Flask, SQLite,
pytest, flake8, and GitHub Actions**. Library staff can add books, issue
and return them, while members can search the catalog. The CI workflow
automatically installs dependencies, checks code quality, and runs
automated tests on pushes and pull requests targeting `main` or
`master`.

------------------------------------------------------------------------

## Table of Contents

-   [Project Overview](#project-overview)
-   [Technology Stack](#technology-stack)
-   [Features](#features)
-   [Project Structure](#project-structure)
-   [Requirements](#requirements)
-   [Run the Project Locally](#run-the-project-locally)
-   [Run the Automated Tests](#run-the-automated-tests)
-   [Run the Code-Quality Check](#run-the-code-quality-check)
-   [API Endpoints](#api-endpoints)
-   [Continuous Integration Workflow](#continuous-integration-workflow)
-   [Test Cases](#test-cases)
-   [GitHub Workflow Demonstration](#github-workflow-demonstration)
-   [Troubleshooting](#troubleshooting)
-   [Group Information](#group-information)

## Project Overview

Manual testing takes time and can miss defects. This project
demonstrates how Continuous Integration can help a development team
check changes consistently. Whenever code is pushed to the configured
branch, GitHub Actions creates a clean runner, sets up Python, installs
the dependencies, runs `flake8`, and executes the `pytest` test suite.

The application uses SQLite to store book details and loan records. The
core business rules are tested automatically.

## Technology Stack

  Technology       Purpose
  ---------------- -----------------------------------------
  Python           Application logic
  Flask            Web framework and HTTP routes
  SQLite           Persistent storage for books and loans
  HTML             Web page structure
  CSS              Web page styling
  pytest           Automated tests
  flake8           Python code-quality/lint checks
  Git and GitHub   Version control and source-code hosting
  GitHub Actions   Automated CI workflow

## Features

-   Add a book with its title, author, and ISBN.
-   Reject duplicate ISBN values.
-   Search the catalog by title or author.
-   Issue an available book to a member.
-   Enforce a maximum of **3 active books per member**.
-   Prevent an already-issued book from being issued again.
-   Return an issued book and calculate a late fine.
-   Calculate fines at **₹5 per day after 14 elapsed days**.
-   Run automated tests and lint checks through GitHub Actions.

### Fine calculation

The application calculates:

`Fine = max(0, days borrowed - 14) × ₹5`

For example, a book returned after 17 elapsed days has a fine of
**₹15**. A return within 14 elapsed days has no fine.

## Project Structure

``` text
Library-Book-Management/
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
├── static/
│   └── style.css           # Website styling
├── templates/
│   └── index.html          # Flask HTML template
├── app.py                  # Flask application and SQLite logic
├── test_app.py             # Automated pytest tests
├── requirements.txt        # Python dependencies
└── .gitignore               # Files excluded from Git
```

The SQLite database (`library.db`) is created locally when the
application initializes. It is intentionally excluded from Git so that
each environment can create its own database.

## Requirements

Install the following before running the project:

-   Python 3.12 or another compatible Python 3 version
-   Git (optional for running locally, required for pushing changes)
-   A web browser
-   VS Code or another code editor (recommended)

Check that Python and Git are available:

``` bash
python --version
git --version
```

## Run the Project Locally

### 1. Clone the repository

Replace `<YOUR-GITHUB-REPOSITORY-URL>` with the HTTPS URL of the group's
GitHub repository.

``` bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd Library-Book-Management
```

If the project is already on your computer, open a terminal in the
project folder instead.

### 2. Create a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

``` bat
.venv\Scripts\activate.bat
```

**Git Bash or macOS/Linux:**

``` bash
python -m venv .venv
source .venv/Scripts/activate
```

On macOS/Linux, use `source .venv/bin/activate`.

### 3. Install dependencies

``` bash
python -m pip install -r requirements.txt
```

### 4. Initialize the database

``` bash
python -c "import app; app.init_db(); print('Database initialized successfully!')"
```

### 5. Start the Flask server

``` bash
python app.py
```

Open this address in your browser:

**http://127.0.0.1:5000**

Keep the terminal running while using the website. To stop the server,
press `Ctrl + C`.

### 6. Use the application

-   Use **Search Catalog** to search by title or author.
-   Use **Add a Book** to add a title, author, and unique ISBN.
-   Use **Issue a Book** with the book's numeric database ID and a
    member ID.
-   Use **Return a Book** with the numeric ID of an actively issued
    book.
-   The return response displays the calculated fine, if any.

The catalog page displays titles, authors, ISBNs, and availability. To
find a book's numeric ID for issue/return operations, open
**http://127.0.0.1:5000/api/books** while the server is running; the
JSON response includes each book's `id`.

> **Note:** This is a mini-project demonstration. It does not include
> authentication, role-based access control, or production deployment.

## Run the Automated Tests

Activate the virtual environment and run:

``` bash
python -m pytest -v
```

The test suite covers successful book creation, duplicate ISBN
rejection, the three-book issue limit, late-fine calculation, no fine
within the allowed period, title search, author search, prevention of
re-issuing an issued book, availability after return, and blank-field
validation.

The tests use a temporary SQLite database for each test, so test records
do not mix with the local library database.

The expected result for the current test suite is **10 passed**.

## Run the Code-Quality Check

Run:

``` bash
python -m flake8 app.py test_app.py --ignore=E501
```

No output means the check passed. The `E501` rule is ignored to avoid
blocking the workflow on line-length warnings; other enabled flake8
checks still run.

## API Endpoints

  -----------------------------------------------------------------------
  Method                  Endpoint                Purpose
  ----------------------- ----------------------- -----------------------
  `GET`                   `/`                     Display the catalog and
                                                  optional search results

  `GET`                   `/api/books`            Return books as JSON;
                                                  supports
                                                  `?q=search-term`

  `POST`                  `/api/books`            Add a book

  `POST`                  `/api/issue`            Issue a book

  `POST`                  `/api/return`           Return a book and
                                                  calculate its fine
  -----------------------------------------------------------------------

Example JSON request to add a book:

``` json
{
  "title": "Python Programming",
  "author": "John Smith",
  "isbn": "LIB-001"
}
```

Example JSON request to issue a book:

``` json
{
  "book_id": 1,
  "member_id": "MEMBER-1"
}
```

Example JSON request to return a book:

``` json
{
  "book_id": 1
}
```

Successful book creation returns HTTP `201`. A duplicate ISBN returns
HTTP `409`. Validation and issue/return errors return HTTP `400`.

## Continuous Integration Workflow

The workflow file is `.github/workflows/ci.yml`.

It runs on:

-   Pushes to `main` or `master`
-   Pull requests targeting `main` or `master`

The CI job runs on `ubuntu-latest` and performs these steps:

1.  **Checkout repository** --- downloads the repository source.
2.  **Set up Python** --- configures Python 3.12.
3.  **Install dependencies** --- installs packages from
    `requirements.txt`.
4.  **Check code quality with flake8** --- checks `app.py` and
    `test_app.py`.
5.  **Run automated tests** --- executes `pytest -v`.

A green check indicates that all workflow steps succeeded. A red cross
means a step failed; open the job logs to inspect the error.

### How to verify CI on GitHub

1.  Push the code to the GitHub repository.
2.  Open the repository's **Actions** tab.
3.  Select **Library Management CI**.
4.  Open the latest run and inspect the **Build and Test** job.
5.  Confirm the lint and pytest steps have passed.

For this project, two successful workflow runs were observed: the
initial project commit and a later commit updating the application
version. This demonstrates that a new push triggers another CI run.

## Test Cases

  Test                                Expected behaviour
  ----------------------------------- ------------------------------
  Add a valid book                    Book is added successfully
  Add a duplicate ISBN                Request is rejected
  Member already has 3 active loans   Fourth issue is rejected
  Return after 17 elapsed days        Fine is ₹15
  Return within 14 elapsed days       Fine is ₹0
  Search by title                     Matching title is returned
  Search by author                    Matching author is returned
  Issue a book twice                  Second issue is rejected
  Return a book                       Book becomes available again
  Add blank book details              Validation error is raised

## GitHub Workflow Demonstration

To demonstrate that CI runs automatically after a new change:

``` bash
git add app.py
git commit -m "Update application version"
git push
```

Then open the GitHub **Actions** tab. A new run should appear for the
new commit. Wait for it to complete and confirm the green check mark.

## Troubleshooting

**PowerShell does not allow virtual-environment activation**

Use Command Prompt and run `.venv\Scripts\activate.bat`, or invoke the
environment's Python directly with `.venv\Scripts\python.exe`.

**Port 5000 is already in use**

Stop the other process using the port, or change the port in the final
`app.run(...)` line of `app.py`.

**GitHub Actions does not start**

Confirm the workflow is located at `.github/workflows/ci.yml`, the
workflow YAML is committed, and the push or pull request targets `main`
or `master`.

**Tests pass locally but fail in GitHub Actions**

Open the failed workflow job, inspect the failing step's log, and
reproduce the command locally. The CI runner uses Ubuntu and Python
3.12.

**Duplicate ISBN response**

ISBN values must be unique. Use a different ISBN when adding another
book.

## Group Information

-   **Course/Subject:** DevOps
-   **Group:** 32
-   **Experiment:** Continuous Integration using GitHub Actions
-   **Project:** Library Book Management System
-   **Team members:** Add the names of all four group members before
    submission.
-   **GitHub repository:** Add the group's repository URL before
    submission.

------------------------------------------------------------------------

## Conclusion

The Library Book Management System demonstrates a basic Continuous
Integration pipeline using GitHub Actions. The application implements
library operations with Flask and SQLite, while pytest checks the main
business rules and flake8 checks code quality. Successful workflow runs
confirm that GitHub Actions can automatically execute these checks after
code changes are pushed to the repository.
