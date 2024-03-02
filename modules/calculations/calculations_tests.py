import unittest
from datetime import datetime
from decimal import Decimal
import calculations as calc



class TestUsdToPln(unittest.TestCase):

    def setUp(self):
        # Sample transactions in USD
        self.transactions = {
            datetime(2023, 1, 1): Decimal('100.00'),
            datetime(2023, 1, 2): Decimal('200.00'),
        }
        # Sample exchange rates
        self.rates = {
            datetime(2023, 1, 1): Decimal('4.00'),
            datetime(2023, 1, 2): Decimal('4.50'),
        }
        # Expected PLN transactions
        self.expected_pln_transactions = {
            datetime(2023, 1, 1): Decimal('400.00'),
            datetime(2023, 1, 2): Decimal('900.00'),
        }

    def test_usd_to_pln(self):
        result = calc.usd_to_pln(self.transactions, self.rates)
        self.assertEqual(result, self.expected_pln_transactions)

if __name__ == '__main__':
    unittest.main()