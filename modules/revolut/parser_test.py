import unittest
from decimal import Decimal
from typing import Dict
from csv_parser import parse_pnl_csv

class TestCSVParser(unittest.TestCase):

    def setUp(self):
        self.test_file_path = 'modules/revolut/Revolut_all_profits_excel.csv'

    def test_parse_pnl_csv(self):
        expected_output = {
            '2021-06-28': Decimal('-0.77'),
            '2021-08-03': Decimal('23.21'),
            '2021-11-08': Decimal('1.46'),
        }
        actual_output = parse_pnl_csv(self.test_file_path)
        
        for date, pnl in expected_output.items():
            self.assertTrue(date in actual_output, f"Date {date} not found in actual output")
            self.assertEqual(actual_output[date], pnl, f"PnL for date {date} does not match expected value")

if __name__ == '__main__':
    unittest.main()
