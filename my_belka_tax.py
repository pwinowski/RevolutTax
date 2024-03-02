from typing import Tuple
from decimal import Decimal
import modules.revolut.csv_parser as revolut
import modules.nbp.nbp as nbp
import modules.calculations.calculations as calc

def print_readable(title,  list_of_tuples: list[Tuple[int, Decimal]]):
    print(title)
    for year, value in list_of_tuples:
        print(f"year: {year} - value: {value:.2f}")

pnl_history = revolut.parse_pnl_csv("modules/revolut/Revolut_all_profits_excel.csv")
exchange_rates = nbp.get_exchange_rates_for_specific_dates(pnl_history.keys())
pnl_in_pln = calc.usd_to_pln(pnl_history, exchange_rates)
pnl_per_year = calc.pnl_per_year(pnl_in_pln)
print_readable("PNL per year", pnl_per_year)
base_for_tax = calc.base_for_taxation_per_year(pnl_per_year)
print_readable("Base for taxation per year", base_for_tax)
tax_amount = calc.tax_amount_per_year(base_for_tax)
print_readable("Tax amount per year", tax_amount)

