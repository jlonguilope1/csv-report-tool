import os
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from csv_report import clean_rows, parse_amount, parse_date, summarize  # noqa: E402


class TestParsing(unittest.TestCase):
    def test_amount_formats(self):
        self.assertEqual(parse_amount("1,234.50"), 1234.5)
        self.assertEqual(parse_amount("1.234,50"), 1234.5)
        self.assertEqual(parse_amount("29,90"), 29.9)
        self.assertEqual(parse_amount("€ 29.90"), 29.9)
        self.assertIsNone(parse_amount("abc"))
        self.assertIsNone(parse_amount(""))

    def test_date_formats(self):
        self.assertEqual(parse_date("2026-01-05"), date(2026, 1, 5))
        self.assertEqual(parse_date("05/01/2026"), date(2026, 1, 5))
        self.assertEqual(parse_date("12.02.2026"), date(2026, 2, 12))
        self.assertIsNone(parse_date("not a date"))


class TestCleaning(unittest.TestCase):
    def test_removes_invalid_and_duplicates(self):
        rows = [
            {"date": "2026-01-05", "product": "a", "amount": "10"},
            {"date": "2026-01-05", "product": "A", "amount": "10"},  # duplicate
            {"date": "bad", "product": "a", "amount": "10"},  # invalid date
            {"date": "2026-01-06", "product": "", "amount": "10"},  # no product
        ]
        cleaned, rejected = clean_rows(rows)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(rejected, 3)

    def test_summary(self):
        rows, _ = clean_rows([
            {"date": "2026-01-05", "product": "a", "amount": "10"},
            {"date": "2026-02-05", "product": "b", "amount": "5"},
        ])
        s = summarize(rows)
        self.assertEqual(s["total"], 15)
        self.assertEqual(s["by_month"], {"2026-01": 10, "2026-02": 5})


if __name__ == "__main__":
    unittest.main()
