import datetime
import unittest
from unittest.mock import patch
import requests
import nbp as nbp

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
        result = nbp.getExchangeRates(2022, 'usd')

        # Assert that the function returned the expected data
        self.assertEqual(result, {datetime.datetime(2022, 1, 1):  4.12, datetime.datetime(2022, 1, 2):  4.13})
        
    @patch('requests.get')
    def test_getExchangeRates_failure(self, mock_get):
        # Mock the response from the API
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError()

        # Call the function with the expected parameters
        with self.assertRaises(requests.HTTPError):
            nbp.getExchangeRates(2022, 'usd')

if __name__ == '__main__':
    unittest.main()