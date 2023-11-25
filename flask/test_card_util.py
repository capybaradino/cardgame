import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from card_util import card_getdatestrnow, card_istimeout


class CardUtilTestCase(unittest.TestCase):
    def test_card_getdatestrnow(self):
        # Test the card_getdatestrnow function
        result = card_getdatestrnow()
        self.assertIsInstance(result, str)
        self.assertEqual(
            len(result), 26
        )  # Assuming the date string format is 'YYYY-MM-DDTHH:MM:SS.mmmmmm'


class TestCardUtil(unittest.TestCase):
    def test_card_istimeout(self):
        with patch("game.getparam") as mock_getparam:
            mock_getparam.return_value = 60

            # Test case 1: Timeout not exceeded
            datestr1 = "2022-01-01T12:00:10.123456"
            datestr2 = "2022-01-01T12:00:20.123456"
            self.assertFalse(card_istimeout(datestr1, datestr2))

            # Test case 2: Timeout exceeded
            datestr1 = "2022-01-01T12:00:00.123456"
            datestr2 = "2022-01-01T12:02:00.123456"
            self.assertTrue(card_istimeout(datestr1, datestr2))

            # Test case 3: Timeout exactly equal
            datestr1 = "2022-01-01T12:00:30.123456"
            datestr2 = "2022-01-01T12:01:30.123456"
            self.assertFalse(card_istimeout(datestr1, datestr2))


if __name__ == "__main__":
    unittest.main()
