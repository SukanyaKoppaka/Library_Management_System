class Member:
    """Represents the local library user/member."""

    def __init__(self, name, email):
        self.name = name.strip()
        self.email = email.strip().lower()

    def to_dict(self):
        return {"name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["email"])

    def __str__(self):
        return f"{self.name} ({self.email})"
