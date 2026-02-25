import unittest
import sys
import os

# Add scripts directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scripts.lib.reporter import generate_markdown_table, generate_progress_bar


class TestReporter(unittest.TestCase):
    def test_generate_markdown_table(self):
        headers = ["Col1", "Col2"]
        rows = [["Val1", "Val2"], ["Val3", "Val4"]]
        table = generate_markdown_table(headers, rows)

        self.assertIn("| Col1 | Col2 |", table)
        self.assertIn("| --- | --- |", table)
        self.assertIn("| Val1 | Val2 |", table)
        self.assertIn("| Val3 | Val4 |", table)

    def test_generate_progress_bar(self):
        bar = generate_progress_bar(50, 100, length=10)
        # Should be roughly half full
        self.assertIn("█████░░░░░", bar)
        self.assertIn("50/100", bar)


if __name__ == "__main__":
    unittest.main()
