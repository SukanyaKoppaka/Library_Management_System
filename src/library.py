from datetime import date, timedelta

from book import Book
from member import Member
from loan import Loan
from storage import load_data, save_data


class Library:
    """Application logic for books, members, borrowing and returns."""

    LOAN_PERIOD_DAYS = 14  # Default chosen for this implementation.

    def __init__(self):
        self.data = load_data()

    def _save(self):
        save_data(self.data)

    def list_books(self):
        return [Book.from_dict(item) for item in self.data["books"]]

    def add_book(self, title, author, genre, isbn):
        values = [title, author, genre, isbn]
        if any(not str(value).strip() for value in values):
            raise ValueError("All book fields are required.")
        isbn = isbn.strip()
        if any(item["isbn"] == isbn for item in self.data["books"]):
            raise ValueError("A book with this ISBN already exists.")
        book = Book(title, author, genre, isbn)
        self.data["books"].append(book.to_dict())
        self._save()
        return book

    def search_books(self, query):
        query = query.strip().casefold()
        if not query:
            raise ValueError("Search text cannot be empty.")
        matches = []
        for item in self.data["books"]:
            searchable = " ".join(
                (item["isbn"], item["title"], item["author"], item["genre"])
            ).casefold()
            if query in searchable:
                matches.append(Book.from_dict(item))
        return matches

    def ensure_member(self, name, email):
        if not name.strip() or not email.strip() or "@" not in email:
            raise ValueError("Enter a valid name and email address.")
        normalized = email.strip().lower()
        for item in self.data["members"]:
            if item["email"].lower() == normalized:
                return Member.from_dict(item)
        member = Member(name, normalized)
        self.data["members"].append(member.to_dict())
        self._save()
        return member

    def borrow_book(self, isbn, member_email):
        isbn = isbn.strip()
        member_email = member_email.strip().lower()
        book = next(
            (item for item in self.data["books"] if item["isbn"] == isbn), None
        )
        if book is None:
            raise ValueError("Book not found.")
        member = next(
            (item for item in self.data["members"]
             if item["email"].lower() == member_email), None
        )
        if member is None:
            raise ValueError("Member not found. Set up the member first.")

        active_loan = any(
            loan["book_isbn"] == isbn and not loan.get("returned", False)
            for loan in self.data["loans"]
        )
        if active_loan:
            raise ValueError("This book is already borrowed.")

        due_date = (date.today() + timedelta(days=self.LOAN_PERIOD_DAYS)).isoformat()
        loan = Loan(isbn, member_email, due_date)
        self.data["loans"].append(loan.to_dict())
        self._save()
        return loan

    def return_book(self, isbn):
        isbn = isbn.strip()
        for loan in reversed(self.data["loans"]):
            if loan["book_isbn"] == isbn and not loan.get("returned", False):
                loan["returned"] = True
                self._save()
                return True
        return False

    def borrowing_history(self, member_email):
        email = member_email.strip().lower()
        return [
            Loan.from_dict(loan)
            for loan in self.data["loans"]
            if loan["member_email"].lower() == email
        ]

    def overdue_loans(self, member_email=None):
        today = date.today()
        result = []
        for item in self.data["loans"]:
            if item.get("returned", False):
                continue
            if member_email and item["member_email"].lower() != member_email.lower():
                continue
            try:
                due = date.fromisoformat(item["due_date"])
            except ValueError:
                continue
            if due < today:
                result.append(Loan.from_dict(item))
        return result

    def book_title(self, isbn):
        for book in self.data["books"]:
            if book["isbn"] == isbn:
                return book["title"]
        return "Unknown book"
