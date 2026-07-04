import unittest
from unittest.mock import patch, Mock
import requests
from src.data_loader import api_data_generator
from src.exceptions import MarketMockError

class TestDataLoader(unittest.TestCase):

    @patch("src.data_loader.requests.get")
    def test_api_data_generator_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            [1704067200000, "100.0", "105.0", "90.0", "102.5"],
            [1704153600000, "102.5", "110.0", "100.0", "108.0"]
        ]
        mock_get.return_value = mock_response

        generator = api_data_generator("BTCUSDT")
        results = list(generator)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["Close"], "102.5")
        self.assertEqual(results[1]["Close"], "108.0")
        mock_get.assert_called_once()

    @patch("src.data_loader.requests.get")
    def test_api_data_generator_network_error(self, mock_get):
        mock_get.side_effect = requests.RequestException()

        generator = api_data_generator("BTCUSDT")
        
        with self.assertRaises(MarketMockError):
            list(generator)

if __name__ == "__main__":
    unittest.main()