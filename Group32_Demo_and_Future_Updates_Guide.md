# Group 32 --- Demonstration & Future Updates Guide

## Library Book Management System + GitHub Actions CI

A concise guide for demonstrating the current project, checking what
works, and planning future improvements.

## 1. Current Project Status

**Verified so far** - The Flask application starts locally and the
library page opens in a browser. - A book was added successfully through
the website. - All **10 pytest tests** passed locally. - The flake8
command passed after fixing the reported warnings. - GitHub Actions
completed **two successful workflow runs** after pushes to `main`.

**What this means:** The core operations and configured CI checks work
for the cases tested. This does not prove every possible input or
production scenario is bug-free.

**Known scope/limitations** - No login, user roles, or production
deployment. - No separate due-date reminder or loan-history interface. -
The website's issue/return forms require the numeric database book ID.
To find IDs, open `http://127.0.0.1:5000/api/books` while the Flask
server is running. - The return API calculates the fine and updates
availability; the main catalog does not show a full loan-history
table. - CI installs dependencies, runs flake8, and runs pytest. It does
not deploy the app or build a standalone executable.

## 2. How to Use the Library System

### Start the application

From the project directory, activate the virtual environment and install
dependencies if needed.

**Windows PowerShell:**

``` powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import app; app.init_db(); print('Database initialized')"
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Keep the terminal open.
Stop the server with `Ctrl + C`.

### Navigate the website

1.  **Search Catalog:** Enter a title or author and click Search. Click
    Clear to show all books.
2.  **Add a Book:** Enter title, author and a unique ISBN, then click
    Add Book. A success/error message appears.
3.  **Find the book ID:** Open `http://127.0.0.1:5000/api/books` in
    another tab. Find the book and note its numeric `id`.
4.  **Issue a Book:** Enter that numeric book ID and a member ID. The
    book must be available, and the member must have fewer than three
    active loans.
5.  **Return a Book:** Enter the numeric ID of an issued book. The
    response displays the fine. A returned book becomes available again.
6.  **Test duplicate ISBN:** Try adding a second book with an ISBN
    already in the database. The request should be rejected.

### Fine rule

`Fine = max(0, elapsed days - 14) × ₹5`

For example, a book returned 17 elapsed days after issue incurs a fine
of ₹15.

**Database note:** The local `library.db` stores records between runs.
The GitHub Actions tests use temporary databases, so CI test data does
not populate your local catalog. The database is ignored by Git and is
not shared with teammates.

## 3. Five Test Cases --- Library System

  ------------------------------------------------------------------------
                     \# Test             Steps            Expected result
  --------------------- ---------------- ---------------- ----------------
                      1 Add/search a     Add a unique     Book is added
                        book             title, author    and appears in
                                         and ISBN; search search results.
                                         by title or      
                                         author.          

                      2 Duplicate ISBN   Add a book, then Duplicate is
                                         try another book rejected;
                                         with the same    original
                                         ISBN.            remains.

                      3 Three-book limit Issue three      First three
                                         different books  succeed; fourth
                                         to one member,   is rejected.
                                         then attempt a   
                                         fourth.          

                      4 Already-issued   Issue a book to  Second issue is
                        book             Member A, then   rejected.
                                         try issuing it   
                                         to Member B      
                                         without          
                                         returning it.    

                      5 Return and fine  Issue a book     Fine is ₹15 and
                                         using a known    the book becomes
                                         date, then       available again.
                                         return it 17     
                                         elapsed days     
                                         later.           
  ------------------------------------------------------------------------

For the fine scenario, the automated test uses fixed dates. The
website's current return form uses today's date, so an exact 17-day
demonstration requires issuing a book 17 days earlier or testing the
return function through pytest.

## 4. Five Test Cases --- GitHub Actions Workflow

  -------------------------------------------------------------------------
                     \# Test             Steps             Expected result
  --------------------- ---------------- ----------------- ----------------
                      1 Push trigger     Commit and push a A new workflow
                                         harmless change   run appears in
                                         to `main`.        Actions.

                      2 Dependency setup Open the run and  The step
                                         inspect **Install completes
                                         dependencies**.   successfully.

                      3 Lint check       Inspect **Check   Green check;
                                         code quality with command exits
                                         flake8**.         successfully.

                      4 Automated tests  Inspect **Run     Pytest completes
                                         automated         with
                                         tests**.          `10 passed`.

                      5 Failure          In a separate     CI turns red for
                        detection        test-only change, the failing
                                         temporarily make  test; after the
                                         an assertion      fix, a new run
                                         incorrect and     passes. Do this
                                         push; then        only when you
                                         revert/fix it.    have time to
                                                           restore the
                                                           code.
  -------------------------------------------------------------------------

The pull-request trigger can also be tested by creating a branch,
pushing it, and opening a pull request targeting `main`. The workflow
should run against the pull request.

## 5. Future Updates / Demonstration Ideas

Use this list as a change log or a menu of future enhancements. Do not
claim an item is implemented until it has actually been added and
tested.

-   [ ] Add a visible book ID to each catalog entry so users do not need
    to open the JSON API.
-   [ ] Add a loan-history page showing member, issue date, return date
    and fine.
-   [ ] Add due-date display and overdue-book indicators.
-   [ ] Add login and separate librarian/member permissions.
-   [ ] Add input validation for ISBN format and more user-friendly
    error messages.
-   [ ] Add tests for missing books, invalid IDs, blank member IDs, and
    date edge cases.
-   [ ] Add pytest coverage reporting to CI.
-   [ ] Add branch protection so pull requests require successful CI
    checks.
-   [ ] Update GitHub Actions action versions when needed to address
    runtime deprecation warnings.
-   [ ] Add a deployment workflow and a production WSGI server if
    deployment is required.

### Demonstration tip

A simple, reliable presentation sequence is:

1.  Open the library website and search the catalog.
2.  Add a book and show it in the catalog.
3.  Open the books JSON endpoint to identify its ID.
4.  Issue and return the book; show the success message and fine
    response.
5.  Open GitHub Actions and show the latest green run, then open the
    pytest and flake8 logs.

## 6. Quick CI Commands

Run locally from the project directory:

``` bash
python -m pytest -v
python -m flake8 app.py test_app.py --ignore=E501
```

Commit and push a change to trigger CI:

``` bash
git add .
git commit -m "Describe your change"
git push
```

Before `git add .`, check `git status` to ensure you are not staging
local database files or unrelated changes.
