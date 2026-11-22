class Loan:
    """Represents a book borrowing record."""

    def __init__(self, book_isbn, member_email, due_date, returned=False):
        self.book_isbn = book_isbn.strip()
        self.member_email = member_email.strip().lower()
        self.due_date = due_date.strip()  # ISO format: YYYY-MM-DD
        self.returned = bool(returned)

    def to_dict(self):
        return {
            "book_isbn": self.book_isbn,
            "member_email": self.member_email,
            "due_date": self.due_date,
            "returned": self.returned,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["book_isbn"],
            data["member_email"],
            data["due_date"],
            data.get("returned", False),
        )
