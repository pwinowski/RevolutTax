from datetime import datetime
from decimal import Decimal
from typing import Dict

def usd_to_pln(transactions: Dict[datetime, Decimal], rates: Dict[datetime, Decimal]) -> Dict[datetime, Decimal]:
    """
    Converts transactions from USD to PLN using exchange rates.

    Args:
        transactions (Dict[datetime, Decimal]): A dictionary containing transactions in USD.
        rates (Dict[datetime, Decimal]): A dictionary containing exchange rates.

    Returns:
        Dict[datetime, Decimal]: A dictionary containing transactions in PLN.
    """
    
    pln_transactions = {}
    
    for date, amount in transactions.items():
        rate = rates[date]
        pln_amount = amount * rate
        pln_transactions[date] = pln_amount
        
    return pln_transactions


def pnl_per_year(transactions: Dict[datetime, Decimal]) -> Dict[int, Decimal]:
    """
    Calculates the PnL per year for each year in the provided transactions.

    Args:
        transactions (Dict[datetime, Decimal]): A dictionary containing transactions.

    Returns:
        Dict[int, Decimal]: A dictionary containing the PnL per year for each year in the provided transactions.
    """

    pnl_per_year = {}

    for date, amount in transactions.items():
        year = date.year
        if year not in pnl_per_year:
            pnl_per_year[year] = amount
        else:
            pnl_per_year[year] += amount

    return pnl_per_year