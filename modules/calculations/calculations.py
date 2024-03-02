from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Tuple



def usd_to_pln(transactions: Dict[datetime, Decimal], rates: Dict[datetime, Decimal]) -> Dict[datetime, Decimal]:
    """
    Converts transactions from USD to PLN using exchange rates.

    Args:
        transactions (Dict[datetime, Decimal]): A dictionary containing transactions in USD.
        rates (Dict[datetime, Decimal]): A dictionary containing exchange rates.

    Returns:
        Dict[datetime, Decimal]: A dictionary containing transactions in PLN.

    Raises:
        KeyError: If a rate for a given date is not found.
    """

    pln_transactions = {}

    for date, amount in transactions.items():
        if date not in rates:
            raise KeyError(f"No rate found for date: {date}")
        rate = rates[date]
        pln_amount = amount * rate
        pln_transactions[date] = pln_amount

    return pln_transactions


def pnl_per_year(transactions: Dict[datetime, Decimal]) -> List[Tuple[int, Decimal]]:
    """
    Calculates the PnL per year for each year in the provided transactions and orders them by year.

    Args:
        transactions (Dict[datetime, Decimal]): A dictionary containing transactions.

    Returns:
        List[Tuple[int, Decimal]]: A list of tuples containing the year and PnL per year, ordered by year.
    """

    pnl_per_year = {}

    for date, amount in transactions.items():
        year = date.year
        if year not in pnl_per_year:
            pnl_per_year[year] = amount
        else:
            pnl_per_year[year] += amount

    return sorted(pnl_per_year.items())

def base_for_taxation_per_year(pnl_per_year: List[Tuple[int, Decimal]]) -> List[Tuple[int, Decimal]]:
    """
    Calculates the base for taxation per year based on the PnL per year.
    WARNING: This is a simplified calculation, that does not take into account that loss can cary over only up to 5 years forward.

    Args:
        pnl_per_year List[Tuple[int, Decimal]]: A List of tuples containing the PnL per year.

    Returns:
        List[Tuple[int, Decimal]]: A List of tuples containing the base for taxation per year.
    """

    base_for_taxation_per_year = []
    carryover_loss = Decimal(0)

    for year, profit in pnl_per_year:
        if profit < 0: # Loss
            carryover_loss += profit
            base_for_taxation_per_year.append((year, Decimal(0)))
        else: # Gain or no change
            if carryover_loss < 0:
                if profit > abs(carryover_loss):
                    base_for_taxation_per_year.append((year, profit + carryover_loss))
                    carryover_loss = Decimal(0)
                else:
                    carryover_loss += profit
                    base_for_taxation_per_year.append((year, Decimal(0)))
            else:
                base_for_taxation_per_year.append((year, profit))

    return base_for_taxation_per_year

def tax_amount_per_year(base_for_taxation_per_year: List[Tuple[int, Decimal]]) -> List[Tuple[int, Decimal]]:
    """
    Calculates the tax amount per year based on the base for taxation per year.

    Args:
        base_for_taxation_per_year List[Tuple[int, Decimal]]: A List of tuples containing the base for taxation per year.

    Returns:
        List[Tuple[int, Decimal]]: A List of tuples containing the tax amount per year.
    """

    tax_amount_per_year = []

    for year, base in base_for_taxation_per_year:
        if base > 0:
            tax_amount_per_year.append((year, base * Decimal(0.19)))
        else:
            tax_amount_per_year.append((year, Decimal(0)))

    return tax_amount_per_year