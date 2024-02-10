import requests

baseURL = "https://api.nbp.pl/api/"

def getExchangeRates(year, currency='usd'):
    """Fetches exchange rates from NBP API"""
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
