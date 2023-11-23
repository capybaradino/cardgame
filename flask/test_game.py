import os
import unittest
from unittest.mock import patch

from game import getparam


class TestGame(unittest.TestCase):
    @patch("game.debug.getdebugparam")
    def test_getparam_with_debugparam(self, mock_getdebugparam):
        key = "some_key"
        expected_result = "debug_value"
        mock_getdebugparam.return_value = expected_result

        result = getparam(key)

        self.assertEqual(result, expected_result)
        mock_getdebugparam.assert_called_once_with(key)

    @patch("game.debug.getdebugparam")
    @patch("configparser.ConfigParser")
    @patch("os.path.isfile")
    def test_getparam_without_debugparam(
        self, mock_isfile, mock_ConfigParser, mock_getdebugparam
    ):
        key = "some_key"
        expected_result = "config_value"
        mock_getdebugparam.return_value = None
        mock_isfile.return_value = True
        mock_ConfigParser.return_value.get.return_value = expected_result

        result = getparam(key)

        self.assertEqual(result, expected_result)
        mock_getdebugparam.assert_called_once_with(key)
        mock_isfile.assert_called_once_with("game.ini")
        mock_ConfigParser.assert_called_once()
        mock_ConfigParser.return_value.read.assert_called_once_with("game.ini")
        mock_ConfigParser.return_value.get.assert_called_once_with("player", key)


if __name__ == "__main__":
    unittest.main()
