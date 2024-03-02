from datetime import datetime, timedelta
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

def usd_to_pln_detailed(transactions: List[Tuple[datetime, datetime, Decimal, Decimal]], rates: Dict[datetime, Decimal]) -> List[Tuple[datetime, datetime, Decimal, Decimal]]:
    """
    Converts transactions from USD to PLN using exchange rates for both the cost basis and the amount.

    Args:
        transactions (list[tuple[datetime, datetime, Decimal, Decimal]]): A list of tuples containing the 'Date acquired', 'Date sold', 'Cost basis', and 'Amount' for each transaction.
        rates (Dict[datetime, Decimal]): A dictionary containing exchange rates.

    Returns:
        list[tuple[datetime, datetime, Decimal, Decimal]]: A list of tuples with the same structure as the input, but with the 'Cost basis' and 'Amount' converted to PLN.

    Raises:
        KeyError: If a rate for a given date is not found.
    """
    converted_transactions = []

    for date_acquired, date_sold, cost_basis, amount in transactions:
        date_preceeding_aquisition = date_acquired - timedelta(days=1)
        date_preceeding_sale = date_sold - timedelta(days=1)
        while date_preceeding_aquisition not in rates:
            date_preceeding_aquisition -= timedelta(days=1)
        while date_preceeding_sale not in rates:
            date_preceeding_sale -= timedelta(days=1)

        rate_acquired = rates[date_preceeding_aquisition]
        rate_sold = rates[date_preceeding_sale]

        pln_cost_basis = cost_basis * rate_acquired
        pln_amount = amount * rate_sold

        converted_transactions.append((date_acquired, date_sold, pln_cost_basis, pln_amount))

    return converted_transactions

def pnl_per_year(transactions: List[Tuple[datetime, datetime, Decimal, Decimal]]) -> List[Tuple[int, Decimal, Decimal, Decimal]]:
    """
    Calculates the PnL per year for each year in the provided transactions and orders them by year.

    Args:
        transactions (List[Tuple[datetime, datetime, Decimal, Decimal]]): A list of tuples containing the 'Date acquired', 'Date sold', 'Cost basis', and 'Amount' for each transaction.

    Returns:
        List[Tuple[int, Decimal, Decimal, Decimal]]: A list of tuples containing the year, total PnL, total Cost basis, and total Amount per year, ordered by year.
    """

    pnl_per_year = {}

    for date_acquired, date_sold, cost_basis, amount in transactions:
        year = date_sold.year
        pnl = amount - cost_basis

        if year not in pnl_per_year:
            pnl_per_year[year] = {'total_pnl': pnl, 'total_cost_basis': cost_basis, 'total_amount': amount}
        else:
            pnl_per_year[year]['total_pnl'] += pnl
            pnl_per_year[year]['total_cost_basis'] += cost_basis
            pnl_per_year[year]['total_amount'] += amount

    # Convert the dictionary to a list of tuples and sort by year
    result = [(year, data['total_pnl'], data['total_cost_basis'], data['total_amount']) for year, data in pnl_per_year.items()]
    result.sort(key=lambda x: x[0]) # Sort by year

    return result

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