# Group 32 --- DevOps Project Chapter

## Library Book Management System with Continuous Integration Using GitHub Actions

**Experiment:** Design and execute a Continuous Integration workflow
using GitHub Actions to automatically build and test an application.

**Project:** Library Book Management System\
**Application stack:** Python, Flask, SQLite, pytest, flake8, Git and
GitHub Actions\
**Group:** 32

------------------------------------------------------------------------

## 1. Introduction

Software teams frequently make changes to application code. If each
change is checked manually, the process can become slow and
inconsistent. A developer may accidentally introduce a defect, overlook
a validation rule, or break a feature that previously worked. When
changes are integrated late, finding the source of the problem can also
become more difficult.

Continuous Integration (CI) addresses this problem by automatically
running a defined set of checks whenever developers push code or open a
pull request. It gives the team quick feedback about whether the latest
change passes the project's quality checks and automated tests.

For this experiment, we developed a Library Book Management System for a
college library. We used Python and Flask for the application, SQLite
for data storage, pytest for automated tests, flake8 for code-quality
checks, and GitHub Actions to automate the CI workflow.

## 2. Problem Statement (PS)

A development team is building an application and wants to automate code
building and testing using GitHub Actions. Manual testing is slow and
can lead to missed errors, affecting software quality. Design a
Continuous Integration workflow that automatically builds and tests the
application on every code commit to ensure reliability.

To demonstrate the solution, Group 32 selected a Library Book Management
System. The application supports basic library operations, and its
business rules provide clear cases for automated testing.

### 2.1 Functional requirements

The application must support the following features:

1.  **Add books:** Store the book's title, author, and ISBN.
2.  **Issue books:** Issue an available book to a library member.
3.  **Issue limit:** Prevent a member from holding more than three
    active book loans at a time.
4.  **Return books:** Record a book's return and calculate any late
    fine.
5.  **Fine calculation:** Charge ₹5 per day after 14 elapsed days.
6.  **Search:** Find books by title or author.
7.  **Duplicate validation:** Reject a book if its ISBN already exists.
8.  **Availability validation:** Prevent a book that is already issued
    from being issued again.

### 2.2 CI requirement

Every push to the configured `main` or `master` branch, and every pull
request targeting either branch, should trigger the workflow. The
workflow installs dependencies, checks code quality, runs automated
tests, and reports success or failure.

## 3. Objectives

-   Develop a basic web application for library book management.
-   Store book and loan information using SQLite.
-   Implement important business rules and validation.
-   Create automated tests for the application's core functionality.
-   Use flake8 to detect common Python code-quality issues.
-   Configure GitHub Actions to run checks automatically on pushes and
    pull requests.
-   Demonstrate that a later code change triggers a new CI run.

## 4. Technology Stack

  -----------------------------------------------------------------------
  Technology                          Role in the project
  ----------------------------------- -----------------------------------
  **Python**                          Main programming language for
                                      application logic and tests.

  **Flask**                           Web framework that serves the HTML
                                      page and provides HTTP API routes.

  **SQLite**                          Lightweight relational database
                                      storing books and loan records in a
                                      local database file.

  **HTML**                            Defines the structure of the
                                      library website.

  **CSS**                             Styles the website and makes the
                                      layout more readable and
                                      responsive.

  **pytest**                          Runs automated tests and reports
                                      whether expected behaviours pass.

  **flake8**                          Checks Python files for common
                                      style and code-quality issues.

  **Git**                             Tracks file changes and records
                                      commits.

  **GitHub**                          Hosts the repository and stores the
                                      project's version history.

  **GitHub Actions**                  Runs the CI workflow automatically
                                      on GitHub-hosted runners.

  **Virtual environment (`venv`)**    Isolates the project's Python
                                      dependencies from other local
                                      Python projects.
  -----------------------------------------------------------------------

### 4.1 Why this stack?

The stack is lightweight and suitable for a college mini-project. Flask
makes it possible to create a web application and API without a large
framework. SQLite avoids the need to install and configure a separate
database server. pytest makes it straightforward to test business rules,
and flake8 provides an additional quality check. GitHub Actions connects
these checks to the team's repository so they run after code changes.

## 5. System Design and Implementation

### 5.1 High-level architecture

``` text
User's browser
     |
     | HTTP request
     v
Flask application (app.py)
     |
     | SQL queries
     v
SQLite database (books and loans)

Developer
     |
     | git commit / git push
     v
GitHub repository
     |
     | push or pull request event
     v
GitHub Actions CI workflow
     |
     +--> Set up Python
     +--> Install dependencies
     +--> Run flake8
     +--> Run pytest
     |
     v
Success or failure status
```

The web application and CI workflow have different responsibilities.
Flask and SQLite serve the library's functionality. GitHub Actions runs
checks against the repository's code in a separate environment.

### 5.2 Database design

The application uses two SQLite tables.

**Books table**

  Field         Purpose
  ------------- ----------------------------------------------------
  `id`          Primary key identifying each book.
  `title`       Book title.
  `author`      Author's name.
  `isbn`        Unique ISBN value.
  `available`   Indicates whether the book is available for issue.

**Loans table**

  -----------------------------------------------------------------------
  Field                               Purpose
  ----------------------------------- -----------------------------------
  `id`                                Primary key identifying each loan.

  `book_id`                           References the book being borrowed.

  `member_id`                         Identifies the member borrowing the
                                      book.

  `issue_date`                        Date the book was issued.

  `return_date`                       Date the book was returned; `NULL`
                                      means the loan is active.

  `fine`                              Fine calculated for the completed
                                      loan.
  -----------------------------------------------------------------------

The database initialization function creates the tables if they do not
already exist. The ISBN column has a unique constraint, so duplicate
ISBN values are rejected by SQLite.

### 5.3 Application logic

The main application logic is implemented in `app.py`.

-   `init_db()` creates the database tables.
-   `add_book()` validates required details and inserts a book.
-   `search_books()` searches the title and author fields.
-   `issue_book()` checks that the book exists and is available, checks
    the member's active-loan count, and records the issue.
-   `return_book()` finds an active loan, calculates the fine, records
    the return, and marks the book available again.

The Flask routes connect these functions to the browser and API clients.
The main page is rendered from `templates/index.html`, while
`static/style.css` provides the presentation.

### 5.4 Fine calculation

The fine is calculated using elapsed calendar days between the issue
date and return date.

**Formula:**

`Fine = max(0, days borrowed − 14) × ₹5`

Examples:

    Elapsed borrowing period   Fine
  -------------------------- ------
                      7 days     ₹0
                     14 days     ₹0
                     15 days     ₹5
                     17 days    ₹15
                     20 days    ₹30

The examples use elapsed days, not inclusive counting of both the issue
and return dates.

## 6. Automated Testing with pytest

Automated tests verify that the program behaves as expected without
requiring a person to repeat each operation manually. The tests in
`test_app.py` use pytest and a temporary SQLite database for isolation.

### 6.1 Test cases

  ------------------------------------------------------------------------
                           No. Test case             Expected result
  ---------------------------- --------------------- ---------------------
                             1 Add a valid book      Book is created
                                                     successfully.

                             2 Add a book with a     Request is rejected.
                               duplicate ISBN        

                             3 Member already has    A fourth issue is
                               three active loans    rejected.

                             4 Return a book after   Fine is ₹15.
                               17 elapsed days       

                             5 Return a book within  Fine is ₹0.
                               14 elapsed days       

                             6 Search by title       Matching title is
                                                     returned.

                             7 Search by author      Matching author is
                                                     returned.

                             8 Issue a book that is  Second issue is
                               already issued        rejected.

                             9 Return an issued book Book becomes
                                                     available again.

                            10 Add blank book        Validation error is
                               details               raised.
  ------------------------------------------------------------------------

### 6.2 Run tests locally

After activating the project's virtual environment and installing its
dependencies, execute:

``` bash
python -m pytest -v
```

The expected result for the current test suite is `10 passed`.

## 7. Code-Quality Checking with flake8

Tests verify application behaviour, while linting helps identify common
code-quality issues. The project runs flake8 against the application and
test files:

``` bash
python -m flake8 app.py test_app.py --ignore=E501
```

The workflow ignores `E501` line-length warnings, while other enabled
flake8 checks remain active. If flake8 reports an error, the developer
can fix it locally and push the corrected code.

## 8. Continuous Integration with GitHub Actions

### 8.1 What is CI?

Continuous Integration is a development practice in which code changes
are integrated into a shared repository frequently, and automated checks
are run to provide quick feedback. CI does not automatically prove that
a program is completely bug-free, but it helps detect problems early and
consistently.

### 8.2 Workflow configuration

The CI configuration is stored in:

`.github/workflows/ci.yml`

GitHub recognises workflow files placed in the `.github/workflows/`
directory. The workflow is configured to run on pushes to `main` or
`master`, and on pull requests targeting those branches.

### 8.3 Workflow steps

1.  **Checkout repository:** `actions/checkout` retrieves the source
    code on the runner.
2.  **Set up Python:** `actions/setup-python` configures Python 3.12.
3.  **Install dependencies:** pip installs packages listed in
    `requirements.txt`.
4.  **Check code quality:** flake8 checks `app.py` and `test_app.py`.
5.  **Run automated tests:** pytest executes the test suite.

The workflow uses an Ubuntu GitHub-hosted runner. The environment is
separate from the developer's laptop, which helps verify that
dependencies and checks work in a clean environment.

### 8.4 How the workflow is triggered

``` text
Developer edits code
        |
        v
git add and git commit
        |
        v
git push to GitHub
        |
        v
GitHub detects a push event
        |
        v
GitHub Actions starts the workflow
        |
        v
Set up Python and install packages
        |
        v
Run flake8
        |
        v
Run pytest
        |
        v
All checks pass? ---- Yes ----> Green check
        |
        No
        v
Red failure status and logs for debugging
```

A successful workflow means every step in the configured job completed
successfully. If a step fails, later steps normally do not run unless
the workflow explicitly says otherwise.

### 8.5 Build versus deployment

This experiment's workflow prepares the Python environment, installs
dependencies, runs lint checks, and tests the code. It does not compile
Python into a standalone binary, package a release artifact, or deploy
the application to a production server. In this context, the
assignment's build stage is represented by environment and dependency
setup.

## 9. Procedure Followed

1.  Created the project folder and Python virtual environment.
2.  Installed Flask, pytest, and flake8.
3.  Created the application, test, template, stylesheet, dependency,
    ignore, and workflow files.
4.  Implemented the Flask application and SQLite database tables.
5.  Implemented book creation, searching, issuing, returning, and fine
    calculation.
6.  Wrote ten automated tests covering the required business rules.
7.  Ran pytest locally and verified that all ten tests passed.
8.  Ran flake8 and fixed the reported warnings.
9.  Created the GitHub repository and initial Git commit.
10. Pushed the project to the `main` branch.
11. Added the GitHub Actions workflow and verified that the CI job
    succeeded.
12. Made a further code change, committed it, and pushed it.
13. Verified that the new push triggered another successful workflow
    run.

## 10. Results and Observations

The project was implemented and pushed to GitHub. The local test suite
reported ten passing tests, and the flake8 check completed without
output after the reported warnings were fixed.

Two successful GitHub Actions workflow runs were observed:

-   The initial project commit triggered the first CI run.
-   A later commit updating the application version triggered a second
    CI run.

Both runs completed successfully. This demonstrates that GitHub Actions
automatically executed the configured checks after a subsequent push,
rather than only during the initial upload.

## 11. Benefits of the Solution

-   Reduces repeated manual checking.
-   Detects certain defects early in the development process.
-   Applies the same configured checks to every matching push or pull
    request.
-   Makes test results and logs visible to all team members.
-   Encourages regular commits and consistent development practices.
-   Provides a clear demonstration of CI using a small, understandable
    application.

## 12. Limitations and Future Scope

The current application is a mini-project demonstration. Possible
improvements include:

-   Add authentication and separate permissions for staff and members.
-   Add a dedicated loan-history page and due-date display.
-   Add stronger validation and more edge-case tests.
-   Add test coverage reporting.
-   Add a code-coverage threshold to CI.
-   Add a production WSGI server and deployment workflow.
-   Add pull-request branch protection requiring CI checks to pass
    before merging.
-   Add database migration support if the schema becomes more complex.

## 13. Conclusion

The Library Book Management System demonstrates how Continuous
Integration can be implemented for a Python web application. Flask
provides the application routes and user interface, SQLite stores book
and loan records, pytest checks the core business rules, and flake8
checks code quality. GitHub Actions automates dependency installation,
linting, and testing when code is pushed or a pull request is opened
against the configured branches.

The successful workflow runs show that the automated checks execute
after code changes and provide a visible result to the team. The
experiment illustrates how CI can improve consistency and help identify
defects earlier in the software development process.

------------------------------------------------------------------------

## Group Information

-   **Subject:** DevOps
-   **Group:** 32
-   **Project:** Library Book Management System
-   **Team members:** Add all four group members' names.
-   **Repository URL:** Add the GitHub repository URL.
