import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

APP_VERSION = "1.0.1"

DATABASE = Path(__file__).with_name("library.db")
LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 5
MAX_BOOKS_PER_MEMBER = 3


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_db() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                available INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL REFERENCES books(id),
                member_id TEXT NOT NULL,
                issue_date TEXT NOT NULL,
                return_date TEXT,
                fine INTEGER NOT NULL DEFAULT 0
            );
        """)


def add_book(title, author, isbn):
    title, author, isbn = title.strip(), author.strip(), isbn.strip()

    if not title or not author or not isbn:
        raise ValueError("Title, author and ISBN are required.")

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO books (title, author, isbn) VALUES (?, ?, ?)",
            (title, author, isbn),
        )
        return cursor.lastrowid


def search_books(query=""):
    with get_db() as db:
        term = f"%{query.strip()}%"
        return db.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
            """,
            (term, term),
        ).fetchall()


def issue_book(book_id, member_id, issue_date=None):
    member_id = member_id.strip()
    issue_date = issue_date or date.today().isoformat()

    if not member_id:
        raise ValueError("Member ID is required.")

    with get_db() as db:
        db.execute("BEGIN IMMEDIATE")

        book = db.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()

        if book is None:
            raise ValueError("Book not found.")

        if not book["available"]:
            raise ValueError("Book is already issued.")

        active_loans = db.execute(
            """
            SELECT COUNT(*) FROM loans
            WHERE member_id = ? AND return_date IS NULL
            """,
            (member_id,),
        ).fetchone()[0]

        if active_loans >= MAX_BOOKS_PER_MEMBER:
            raise ValueError("A member cannot borrow more than 3 books.")

        db.execute(
            "INSERT INTO loans (book_id, member_id, issue_date) "
            "VALUES (?, ?, ?)",
            (book_id, member_id, issue_date),
        )
        db.execute(
            "UPDATE books SET available = 0 WHERE id = ?", (book_id,)
        )


def return_book(book_id, return_date=None):
    return_date = return_date or date.today().isoformat()

    with get_db() as db:
        loan = db.execute(
            """
            SELECT * FROM loans
            WHERE book_id = ? AND return_date IS NULL
            ORDER BY id DESC LIMIT 1
            """,
            (book_id,),
        ).fetchone()

        if loan is None:
            raise ValueError("No active issue found for this book.")

        days_borrowed = (
            date.fromisoformat(return_date) - date.fromisoformat(loan["issue_date"])
        ).days

        if days_borrowed < 0:
            raise ValueError("Return date cannot be before issue date.")

        fine = max(0, days_borrowed - LOAN_PERIOD_DAYS) * FINE_PER_DAY

        db.execute(
            "UPDATE loans SET return_date = ?, fine = ? WHERE id = ?",
            (return_date, fine, loan["id"]),
        )
        db.execute(
            "UPDATE books SET available = 1 WHERE id = ?", (book_id,)
        )

        return fine


@app.route("/")
def index():
    books = search_books(request.args.get("q", ""))
    return render_template("index.html", books=books)


@app.route("/api/books", methods=["GET", "POST"])
def books_api():
    if request.method == "GET":
        books = search_books(request.args.get("q", ""))
        return jsonify([dict(book) for book in books])

    data = request.get_json(silent=True) or request.form

    try:
        book_id = add_book(
            data.get("title", ""),
            data.get("author", ""),
            data.get("isbn", ""),
        )
        return jsonify({"message": "Book added", "id": book_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "ISBN already exists."}), 409
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/issue", methods=["POST"])
def issue_api():
    data = request.get_json(silent=True) or request.form

    try:
        issue_book(
            int(data.get("book_id", "")),
            data.get("member_id", ""),
        )
        return jsonify({"message": "Book issued successfully."}), 200
    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/return", methods=["POST"])
def return_api():
    data = request.get_json(silent=True) or request.form

    try:
        fine = return_book(int(data.get("book_id", "")))
        return jsonify({"message": "Book returned.", "fine": fine}), 200
    except (ValueError, TypeError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
