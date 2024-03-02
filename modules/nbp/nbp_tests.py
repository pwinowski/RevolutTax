import datetime
import unittest
from unittest.mock import patch
import requests
import nbp

class TestGetExchangeRates(unittest.TestCase):

    @patch('requests.get')
    def test_getExchangeRates_success(self, mock_get):
        # Mock the response from the API
        mock_response = {
            "rates": [
                {"effectiveDate": "2022-01-01", "mid":  4.12},
                {"effectiveDate": "2022-01-02", "mid":  4.13}
            ]
        }
        mock_get.return_value.status_code =  200
        mock_get.return_value.json.return_value = mock_response

        # Call the function with the expected parameters
        result = nbp.get_exchange_rates(2022, 'usd')

        # Assert that the function returned the expected data
        self.assertEqual(result, {datetime.datetime(2022, 1, 1):  4.12, datetime.datetime(2022, 1, 2):  4.13})
        
    @patch('requests.get')
    def test_getExchangeRates_failure(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError()

        # Call the function with the expected parameters
        with self.assertRaises(requests.HTTPError):
            nbp.get_exchange_rates(2022, 'usd')

    def test_getExchangeRatesForSpecificDates_e2e(self):
        # Define the dates for which to fetch exchange rates
        dates = [datetime.datetime(2022, 1, 4),
                 datetime.datetime(2023, 3, 5),
                 datetime.datetime(2023, 3, 7)]
        currency = 'usd'

        # Call the function with the specific dates
        result = nbp.get_exchange_rates_for_specific_dates(dates, currency)

        # Print the results
        print(f"Exchange rates for {currency} on:")
        for date, rate in result.items():
            print(f"{date}: {rate}")

        # Assert that the HTTP request was successful
        # Since we're making a real API call, we can't directly assert the status code.
        # However, if the function doesn't raise an exception, we can assume the request was successful.
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()