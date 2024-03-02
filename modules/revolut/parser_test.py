import datetime
import unittest
from decimal import Decimal
from csv_parser import parse_pnl_csv

class TestCSVParser(unittest.TestCase):

    def setUp(self):
        self.test_file_path = 'modules/revolut/Revolut_all_profits_excel.csv'

    def test_parse_pnl_csv(self):
        expected_output = {
            datetime.datetime(2021, 6, 28): Decimal('-0.77'),
            datetime.datetime(2021, 8, 3): Decimal('23.21'),
            datetime.datetime(2021, 11, 8): Decimal('1.46'),
        }
        actual_output = parse_pnl_csv(self.test_file_path)
        
        for date, pnl in expected_output.items():
            self.assertTrue(date in actual_output, f"Date {date} not found in actual output")
            self.assertEqual(actual_output[date], pnl, f"PnL for date {date} does not match expected value")

if __name__ == '__main__':
    unittest.main()