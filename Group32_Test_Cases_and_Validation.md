# Group 32 --- Library Book Management System

## Test Cases and Validation Record

**Project:** Library Book Management System\
**Experiment:** Continuous Integration using GitHub Actions\
**Technology stack:** Python, Flask, SQLite, pytest, flake8, GitHub
Actions

------------------------------------------------------------------------

## 1. Test Summary

  -----------------------------------------------------------------------
  Test ID           Requirement /     Validation method Recorded result
                    Feature                             
  ----------------- ----------------- ----------------- -----------------
  TC-01             Maximum three     Manual            Reported
                    active books per  application test  successful;
                    member                              retain evidence
                                                        of three
                                                        successful issues
                                                        and rejection of
                                                        the fourth to
                                                        demonstrate the
                                                        full limit

  TC-02             Fine after 14     Automated pytest  PASS --- 17
                    days              tests             elapsed days
                                                        produces ₹15

  TC-02A            No fine within 14 Automated pytest  PASS --- fine is
                    days              test              ₹0 within the
                                                        14-day period

  TC-03A            Search by title   Manual            PASS --- correct
                                      application test  book appeared

  TC-03B            Search by author  Manual            PASS --- correct
                                      application test  book appeared

  TC-04             Reject duplicate  Manual            PASS ---
                    ISBN              application test  duplicate was
                                                        rejected with an
                                                        error

  TC-05             Prevent issuing   Manual UI         PARTIALLY
                    an already-issued inspection        VERIFIED ---
                    book                                issued book
                                                        disappeared from
                                                        the Issue
                                                        dropdown and
                                                        appeared in the
                                                        Return dropdown;
                                                        direct backend
                                                        rejection was not
                                                        independently
                                                        verified during
                                                        this session

  TC-06             Return an issued  Manual            PASS --- return
                    book              application test  operation
                                                        succeeded

  TC-06A            Returned book     UI validation     Confirm the book
                    becomes available                   reappears in the
                    again                               Issue dropdown;
                                                        record PASS once
                                                        observed

  TC-06B            Fine shown in     UI validation     Not independently
                    return response                     recorded during
                                                        this session

  TC-07             Continuous        GitHub Actions    PASS --- latest
                    Integration                         workflow run
                    workflow                            succeeded;
                                                        dependency
                                                        installation,
                                                        flake8, and
                                                        pytest steps
                                                        passed
  -----------------------------------------------------------------------

**Note:** Results reflect what was observed or reported during the test
session. Do not mark an item fully passed until its expected behavior
has been verified.

------------------------------------------------------------------------

## 2. Detailed Test Cases

### TC-01 --- Maximum borrowing limit

**Objective:** Verify that a member cannot borrow more than three books
simultaneously.

**Test data:** Member ID `MEMBER-TEST-001`; four distinct books
available at the start of the test.

**Procedure:** 1. Issue the first book to the test member. 2. Issue a
second distinct book to the same member. 3. Issue a third distinct book
to the same member. 4. Attempt to issue a fourth distinct book to the
same member.

**Expected result:** The first three issues succeed. The fourth issue is
rejected.

**Recorded result:** The user reported the test as successful. Keep
evidence showing the three successful issues and the rejected fourth
issue to substantiate the full requirement.

### TC-02 --- Late-return fine calculation

**Objective:** Verify the fine is ₹5 per day after the 14-day borrowing
period.

**Test scenario:** Return a book after 17 elapsed days.

**Expected calculation:**

`Fine = max(0, days borrowed - 14) × ₹5`

`Fine = (17 - 14) × ₹5 = ₹15`

**Automated validation:**
`test_fine_is_five_rupees_per_day_after_fourteen_days` --- PASS.

### TC-02A --- No fine within the allowed period

**Objective:** Verify that a return within 14 days does not incur a
fine.

**Expected result:** ₹0.

**Automated validation:** `test_no_fine_within_fourteen_days` --- PASS.

**Evidence:** The terminal screenshot shared during the session showed
both fine-related tests passed, with 2 passed and 8 deselected.

### TC-03A --- Search by title

**Objective:** Verify that catalog search finds a book by title.

**Procedure:** Search for the exact title of a book already in the
catalog.

**Expected result:** The matching book appears in search results.

**Recorded result:** PASS --- the user confirmed the correct book
appeared.

### TC-03B --- Search by author

**Objective:** Verify that catalog search finds books by author.

**Procedure:** Search using an author name associated with a book in the
catalog.

**Expected result:** The matching book appears in search results.

**Recorded result:** PASS --- the user confirmed the search worked.

### TC-04 --- Duplicate ISBN rejection

**Objective:** Prevent two books from being registered with the same
ISBN.

**Procedure:** Attempt to add a book with a different title and author
but an ISBN already present in the catalog.

**Expected result:** The new record is rejected and an error message is
displayed.

**Recorded result:** PASS --- the user confirmed the error appeared.

### TC-05 --- Prevent duplicate issuing

**Objective:** Prevent a book that is already issued from being issued
again.

**UI validation performed:** The issued book appeared in the Return
dropdown and was absent from the Issue dropdown.

**Recorded result:** PARTIALLY VERIFIED. This confirms the UI reflects
availability. A direct attempt to issue the same book again and observe
backend rejection was not independently completed during this session.

### TC-06 --- Return a book

**Objective:** Verify that an issued book can be returned successfully.

**Procedure:** Select an issued book in the Return dropdown and submit
the return form.

**Expected result:** The return operation succeeds and the book becomes
available again.

**Recorded result:** PASS for successful return. Confirm that the book
reappears in the Issue dropdown if this has not already been observed.

### TC-07 --- GitHub Actions Continuous Integration

**Objective:** Verify that the CI workflow installs dependencies, checks
code style, and runs automated tests.

**Workflow steps verified:** 1. Check out repository. 2. Set up Python.
3. Install dependencies from `requirements.txt`. 4. Run `flake8`. 5. Run
`pytest`.

**Recorded result:** PASS --- the user confirmed the latest GitHub
Actions workflow run was green and all relevant steps passed.

------------------------------------------------------------------------

## 3. Evidence Checklist

Add screenshots to an `evidence/` folder if available:

-   [ ] `TC-01-borrowing-limit.png` --- three successful issues and
    fourth rejected
-   [x] `TC-02-fine-tests.png` --- terminal screenshot showing the two
    fine tests passing
-   [ ] `TC-03-search-title.png`
-   [ ] `TC-03-search-author.png`
-   [ ] `TC-04-duplicate-isbn.png`
-   [ ] `TC-05-duplicate-issue.png` --- direct backend rejection, if
    tested
-   [ ] `TC-06-return-book.png`
-   [ ] `TC-06-availability-restored.png`
-   [ ] `TC-07-github-actions.png`

Only add screenshots that you actually captured. Check your local
screenshots folder before marking evidence present in the repository.

------------------------------------------------------------------------

## 4. How to Run the Automated Tests

From the project root with the virtual environment activated:

``` powershell
python -m pytest -v
```

Run fine-related tests only:

``` powershell
python -m pytest -v test_app.py -k fine
```

Run linting:

``` powershell
python -m flake8 app.py test_app.py --ignore=E501
```

Record actual command output when collecting new evidence.

------------------------------------------------------------------------

## 5. Final Notes

-   Manual UI checks and automated tests are different forms of
    evidence; record them separately.
-   A successful GitHub Actions run verifies the workflow passed for the
    commit that was tested.
-   Avoid including real personal information in test member IDs or
    screenshots.
-   Update this document if further validation changes a result from
    partially verified to passed.
