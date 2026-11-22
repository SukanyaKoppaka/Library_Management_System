class Book:
    """Represents a book in the library collection."""

    def __init__(self, title, author, genre, isbn):
        self.title = title.strip()
        self.author = author.strip()
        self.genre = genre.strip()
        self.isbn = isbn.strip()

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "isbn": self.isbn,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["author"], data["genre"], data["isbn"])

    def __str__(self):
        return (
            f"{self.title} | Author: {self.author} | Genre: {self.genre} "
            f"| ISBN: {self.isbn}"
        )
