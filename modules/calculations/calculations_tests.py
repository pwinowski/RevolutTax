import unittest
from datetime import datetime
from decimal import Decimal
import calculations as calc

class CalculationTests(unittest.TestCase):

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

    def test_pnl_per_year(self):
        # Sample transactions
        transactions = {
            datetime(2023, 1, 1): Decimal('100.00'),
            datetime(2023, 1, 2): Decimal('200.00'),
            datetime(2024, 1, 1): Decimal('300.00'),
            datetime(2024, 1, 2): Decimal('400.00'),
        }
        # Expected PnL per year
        expected_pnl_per_year = {
            2023: Decimal('300.00'),
            2024: Decimal('700.00'),
        }
    
        result = calc.pnl_per_year(transactions)
        self.assertEqual(result, expected_pnl_per_year)

    def test_pnl_per_year_with_losses(self):
        # Sample transactions with losses
        transactions = {
            datetime(2023, 1, 1): Decimal('100.00'),
            datetime(2023, 1, 2): Decimal('-200.00'), # Loss
            datetime(2024, 1, 1): Decimal('300.00'),
            datetime(2024, 1, 2): Decimal('-400.00'), # Loss
        }
        # Expected PnL per year
        expected_pnl_per_year = {
            2023: Decimal('-100.00'), # Loss
            2024: Decimal('-100.00'), # Loss
        }
    
        result = calc.pnl_per_year(transactions)
        self.assertEqual(result, expected_pnl_per_year)

if __name__ == '__main__':
    unittest.main()