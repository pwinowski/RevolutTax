from typing import Tuple
from decimal import Decimal
import modules.revolut.csv_parser as revolut
import modules.nbp.nbp as nbp
import modules.calculations.calculations as calc

def print_readable_long(title,  list_of_tuples: list[Tuple[int, Decimal, Decimal, Decimal]]):
    print(title)
    for year, profit, spent, gained in list_of_tuples:
        print(f"year: {year} - profit: {profit:.2f}, spent: {spent:.2f}, gained: {gained:.2f}")

def print_readable(title,  list_of_tuples: list[Tuple[int, Decimal]]):
    print(title)
    for year, value in list_of_tuples:
        print(f"year: {year} - value: {value:.2f}")

pnl_history = revolut.parse_pnl_csv_detailed("modules/revolut/Revolut_all_profits_excel.csv")
rates2020 = nbp.get_exchange_rates(2020, "usd")
rates2021 = nbp.get_exchange_rates(2021, "usd")
rates2022 = nbp.get_exchange_rates(2022, "usd")
rates2023 = nbp.get_exchange_rates(2023, "usd")
exchange_rates = {**rates2020, **rates2021, **rates2022, **rates2023}
transactions_pln = calc.usd_to_pln_detailed(pnl_history, exchange_rates)
pnl_per_year = calc.pnl_per_year(transactions_pln)
print_readable_long("PNL per year", pnl_per_year)
base_for_tax = calc.base_for_taxation_per_year([(year, profit) for year, profit, _, _ in pnl_per_year])
print_readable("Base for taxation per year", base_for_tax)
tax_amount = calc.tax_amount_per_year(base_for_tax)
print_readable("Tax amount per year", tax_amount)

