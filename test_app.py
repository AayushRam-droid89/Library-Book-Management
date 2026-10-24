import pytest

import app as library


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Give every test its own temporary SQLite database.
    test_database = tmp_path / "test_library.db"
    monkeypatch.setattr(library, "DATABASE", test_database)
    library.init_db()

    library.app.config["TESTING"] = True

    with library.app.test_client() as test_client:
        yield test_client


@pytest.fixture
def add_sample_book():
    def _add(title="Python Basics", author="John Smith", isbn="ISBN-001"):
        return library.add_book(title, author, isbn)

    return _add


def test_add_book_success(client):
    response = client.post(
        "/api/books",
        json={
            "title": "Python Basics",
            "author": "John Smith",
            "isbn": "ISBN-001",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "Book added"


def test_duplicate_isbn_rejected(client, add_sample_book):
    add_sample_book()

    response = client.post(
        "/api/books",
        json={
            "title": "Another Book",
            "author": "Jane Smith",
            "isbn": "ISBN-001",
        },
    )

    assert response.status_code == 409
    assert "ISBN already exists" in response.get_json()["error"]


def test_member_cannot_borrow_more_than_three_books(
    client, add_sample_book
):
    book_ids = [
        add_sample_book(title=f"Book {number}", isbn=f"ISBN-{number}")
        for number in range(1, 5)
    ]

    for book_id in book_ids[:3]:
        library.issue_book(book_id, "MEMBER-1", "2026-01-01")

    with pytest.raises(ValueError, match="more than 3"):
        library.issue_book(book_ids[3], "MEMBER-1", "2026-01-01")


def test_fine_is_five_rupees_per_day_after_fourteen_days(
    client, add_sample_book
):
    book_id = add_sample_book()

    library.issue_book(book_id, "MEMBER-1", "2026-01-01")

    # January 18 is 17 elapsed days after January 1.
    fine = library.return_book(book_id, "2026-01-18")

    assert fine == 15


def test_no_fine_within_fourteen_days(client, add_sample_book):
    book_id = add_sample_book()

    library.issue_book(book_id, "MEMBER-1", "2026-01-01")

    fine = library.return_book(book_id, "2026-01-15")

    assert fine == 0


def test_search_by_title(client, add_sample_book):
    add_sample_book("Python Basics", "John Smith", "ISBN-001")
    add_sample_book("Java Programming", "Jane Doe", "ISBN-002")

    results = library.search_books("Python")

    assert len(results) == 1
    assert results[0]["title"] == "Python Basics"


def test_search_by_author(client, add_sample_book):
    add_sample_book("Python Basics", "John Smith", "ISBN-001")
    add_sample_book("Java Programming", "Jane Doe", "ISBN-002")

    results = library.search_books("Jane Doe")

    assert len(results) == 1
    assert results[0]["author"] == "Jane Doe"


def test_already_issued_book_cannot_be_issued_again(
    client, add_sample_book
):
    book_id = add_sample_book()

    library.issue_book(book_id, "MEMBER-1", "2026-01-01")

    with pytest.raises(ValueError, match="already issued"):
        library.issue_book(book_id, "MEMBER-2", "2026-01-01")


def test_returned_book_becomes_available_again(client, add_sample_book):
    book_id = add_sample_book()

    library.issue_book(book_id, "MEMBER-1", "2026-01-01")
    library.return_book(book_id, "2026-01-05")

    # Another member can borrow the book after it is returned.
    library.issue_book(book_id, "MEMBER-2", "2026-01-06")


def test_blank_book_details_are_rejected(client):
    with pytest.raises(ValueError, match="required"):
        library.add_book("", "John Smith", "ISBN-001")
