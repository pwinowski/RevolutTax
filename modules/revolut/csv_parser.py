import csv
from decimal import Decimal
from typing import Dict

def parse_pnl_csv(file_path: str) -> Dict[str, Decimal]:
    """
    Parses a CSV file containing profit and loss data and aggregates the realized PnL values by date.

    Args:
        file_path (str): The path to the CSV file to parse.

    Returns:
        Dict[str, Decimal]: A dictionary where keys are sell dates (as strings) and values are the total realized PnL for each date.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        KeyError: If the CSV file does not contain the expected columns ('Date sold' and 'Realised PnL').
        ValueError: If the 'Realised PnL' value cannot be converted to a Decimal.

    Example usage:
        pnl_data = parse_pnl_csv('/path/to/your/csvfile.csv')
        print(pnl_data)  # Output might look like: {'2021-06-28': Decimal('-0.77'), ...}
    """
    realised_pnls: Dict[str, Decimal] = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_sold: str = row['Date sold']
            realised_pnl: Decimal = Decimal(row['Realised PnL'])
            if date_sold not in realised_pnls:
                realised_pnls[date_sold] = realised_pnl
            else:
                realised_pnls[date_sold] += realised_pnl
    return realised_pnls