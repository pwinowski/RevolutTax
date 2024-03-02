import requests
from typing import Dict
from decimal import Decimal
from datetime import datetime
from typing import List

baseURL = "https://api.nbp.pl/api/"

def get_exchange_rates(year: int, currency: str = 'usd') -> Dict[datetime, Decimal]:
    """
    Fetches exchange rates from the NBP API for a specific year and currency.

    Args:
        year (int): The year for which to fetch exchange rates.
        currency (str, optional): The currency code for which to fetch exchange rates. Defaults to 'usd'.

    Returns:
        Dict[datetime, Decimal]: A dictionary mapping dates to exchange rate values for the specified year and currency.
            The keys are datetime objects representing dates, and the values are Decimals.

    Raises:
        requests.HTTPError: If the request to the NBP API fails with an HTTP error status code.
        Exception: If any other exception occurs during the request or processing of the data.
    """
    endpoint = f"exchangerates/rates/a/{currency}/"
    try:
        startDate = f"{year}-01-01"
        endDate = f"{year}-12-31"
        urlParams = f"/{startDate}/{endDate}/?format=json"
        url = baseURL + endpoint + urlParams
        http_response = requests.get(url)
        http_response.raise_for_status() # Raise an HTTPError if the status code indicates an error
        jsonData = http_response.json()
        return {datetime.strptime(item["effectiveDate"], '%Y-%m-%d'): Decimal(item["mid"]) for item in jsonData["rates"]}
    except requests.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
        raise # Let the exception propagate
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def get_exchange_rates_for_specific_dates(dates: List[datetime], currency: str = 'usd') -> Dict[datetime, Decimal]:
    """
    Fetches exchange rates from the NBP API for a list of specific dates and currency.

    Args:
        dates (List[datetime]): A list of datetime objects representing the dates for which to fetch exchange rates.
        currency (str, optional): The currency code for which to fetch exchange rates. Defaults to 'usd'.

    Returns:
        Dict[datetime, Decimal]: A dictionary mapping dates to exchange rate values for the specified dates and currency.
            The keys are datetime objects representing dates, and the values are Decimals.

    Raises:
        requests.HTTPError: If the request to the NBP API fails with an HTTP error status code other than 404.
        Exception: If any other exception occurs during the request or processing of the data.
    """
    endpoint = f"exchangerates/rates/a/{currency}/"
    exchange_rates = {}

    for date in dates:
        formatted_date = date.strftime('%Y-%m-%d')
        url = f"{baseURL}{endpoint}{formatted_date}/?format=json"
        try:
            http_response = requests.get(url)
            if http_response.status_code == 404:
                print(f"No data available for {currency} on {formatted_date}")
                continue  # Skip this date and move to the next
            http_response.raise_for_status()  # This will raise an HTTPError if the status code indicates an error other than 404
            jsonData = http_response.json()
            exchange_rates[date] = Decimal(jsonData["rates"][0]["mid"])
        except requests.HTTPError as e:
            print(f"An HTTP error occurred for date {formatted_date}: {e}")
        except Exception as e:
            print(f"An error occurred for date {formatted_date}: {e}")

    return exchange_rates
    