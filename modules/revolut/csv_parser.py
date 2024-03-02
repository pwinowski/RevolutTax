import csv
from decimal import Decimal
from typing import Dict
from datetime import datetime

def parse_pnl_csv(file_path: str) -> Dict[datetime, Decimal]:
    """
    Parses a CSV file containing profit and loss data and aggregates the realized PnL values by date.

    Args:
        file_path (str): The path to the CSV file to parse.

    Returns:
        Dict[datetime, Decimal]: A dictionary where keys are sell dates (as datetime objects) and values are the total realized PnL for each date.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        KeyError: If the CSV file does not contain the expected columns ('Date sold' and 'Realised PnL').
        ValueError: If the 'Realised PnL' value cannot be converted to a Decimal.
    """
    realised_pnls: Dict[datetime, Decimal] = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_sold: datetime = datetime.strptime(row['Date sold'], '%Y-%m-%d')
            realised_pnl: Decimal = Decimal(row['Realised PnL'])
            if date_sold not in realised_pnls:
                realised_pnls[date_sold] = realised_pnl
            else:
                realised_pnls[date_sold] += realised_pnl
    return realised_pnls