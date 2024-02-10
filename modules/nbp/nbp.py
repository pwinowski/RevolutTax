import requests

baseURL = "https://api.nbp.pl/api/"

def getExchangeRates(year, currency='usd'):
    """
    Fetches exchange rates from the NBP API for a specific year and currency.

    Args:
        year (int): The year for which to fetch exchange rates.
        currency (str, optional): The currency code for which to fetch exchange rates. Defaults to 'usd'.

    Returns:
        dict: A dictionary mapping dates to exchange rate values for the specified year and currency.
            The keys are strings representing dates in the format 'YYYY-MM-DD', and the values are floats.

    Raises:
        requests.HTTPError: If the request to the NBP API fails with an HTTP error status code.
        Exception: If any other exception occurs during the request or processing of the data.

    Example:
        >>> nbp.getExchangeRates(2023, 'eur')
        {'2023-01-01':  4.50, '2023-01-02':  4.55, ...}
    """
    endpoint = f"exchangerates/rates/a/{currency}/"
    try:
        startDate = f"{year}-01-01"
        endDate = f"{year}-12-31"
        urlParams = f"/{startDate}/{endDate}/?format=json"
        url = baseURL + endpoint + urlParams
        http_response = requests.get(url)
        http_response.raise_for_status()  # Raise an HTTPError if the status code indicates an error
        jsonData = http_response.json()
        return {item["effectiveDate"]: float(item["mid"]) for item in jsonData["rates"]}
    except requests.HTTPError as e:
        print(f"An HTTP error occurred: {e}")
        raise  # Let the exception propagate
    except Exception as e:
        print(f"An error occurred: {e}")
        raise  # Let the exception propagate
