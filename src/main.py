"""Console entry point for the Library Management System."""

import re

from library import Library


def prompt_non_empty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def print_books(books):
    if not books:
        print("No books found.")
        return
    for number, book in enumerate(books, start=1):
        print(f"{number}. {book}")


def main():
    try:
        library = Library()
    except RuntimeError as exc:
        print(f"Startup error: {exc}")
        return

    current_member_email = None
    print("Welcome to the Library Management System!")

    while True:
        print("\n========== LIBRARY MENU ==========")
        print("1. List books")
        print("2. Search books")
        print("3. Borrow book")
        print("4. Return book")
        print("5. View borrowing history")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()

        try:
            if choice == "1":
                print_books(library.list_books())

            elif choice == "2":
                query = prompt_non_empty("Enter ISBN or keyword: ")
                print_books(library.search_books(query))

            elif choice == "3":
                isbn = prompt_non_empty("Enter book ISBN: ")
                # The PRD defines a single local user. Ask for the member
                # profile the first time borrowing is attempted.
                if current_member_email is None:
                    name = prompt_non_empty("Enter your name: ")
                    while True:
                        email = prompt_non_empty("Enter your email: ")
                        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                            break
                        print("Please enter a valid email address.")
                    member = library.ensure_member(name, email)
                    current_member_email = member.email
                loan = library.borrow_book(isbn, current_member_email)
                print(f"Book borrowed successfully. Due date: {loan.due_date}")

            elif choice == "4":
                isbn = prompt_non_empty("Enter book ISBN to return: ")
                if library.return_book(isbn):
                    print("Book returned successfully.")
                else:
                    print("No active loan found for that ISBN.")

            elif choice == "5":
                if current_member_email is None:
                    print("No member profile in this session. Borrow a book first.")
                    continue
                history = library.borrowing_history(current_member_email)
                if not history:
                    print("No borrowing history found.")
                else:
                    for loan in history:
                        status = "Returned" if loan.returned else "Borrowed"
                        overdue = (
                            " (OVERDUE)"
                            if not loan.returned
                            and loan in library.overdue_loans(current_member_email)
                            else ""
                        )
                        print(
                            f"{library.book_title(loan.book_isbn)} | "
                            f"ISBN: {loan.book_isbn} | Due: {loan.due_date} | "
                            f"Status: {status}{overdue}"
                        )

            elif choice == "6":
                print("Thank you for using the Library Management System.")
                break

            else:
                print("Invalid option. Please choose a number from 1 to 6.")

        except (ValueError, RuntimeError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()
