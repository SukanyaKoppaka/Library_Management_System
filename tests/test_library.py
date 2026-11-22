import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import storage
from library import Library


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_path = Path(self.temp_dir.name) / "data.json"
        self.patcher = patch.object(storage, "DATA_FILE", self.data_path)
        self.patcher.start()
        storage.save_data(storage.empty_data())
        self.library = Library()
        self.library.add_book("The Hobbit", "J.R.R. Tolkien", "Fantasy", "111")
        self.library.ensure_member("Test User", "test@example.com")

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_list_and_search_books(self):
        self.assertEqual(len(self.library.list_books()), 1)
        self.assertEqual(len(self.library.search_books("hobbit")), 1)
        self.assertEqual(len(self.library.search_books("999")), 0)

    def test_duplicate_isbn_rejected(self):
        with self.assertRaises(ValueError):
            self.library.add_book("Other", "Author", "Genre", "111")

    def test_borrow_and_return(self):
        loan = self.library.borrow_book("111", "test@example.com")
        self.assertTrue(loan.due_date)
        with self.assertRaises(ValueError):
            self.library.borrow_book("111", "test@example.com")
        self.assertTrue(self.library.return_book("111"))
        self.assertFalse(self.library.return_book("111"))

    def test_history(self):
        self.library.borrow_book("111", "test@example.com")
        self.assertEqual(len(self.library.borrowing_history("test@example.com")), 1)


if __name__ == "__main__":
    unittest.main()
