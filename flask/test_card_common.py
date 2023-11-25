import unittest
from unittest.mock import MagicMock, Mock, patch

from card_common import judge


class TestCardCommon(unittest.TestCase):
    def test_judge(self):
        # Test case 1: Player 1 HP <= 0
        sid = 1
        playview = Mock()
        playview.p1hp = 0
        playview.p2hp = 10
        playdata = Mock()
        playview.playdata = playdata

        with patch("card_common.Play_view", return_value=playview):
            judge(sid)
            playdata.gameover.assert_called_once_with(sid)

        # Test case 2: Player 2 HP <= 0
        sid = 1
        playview = Mock()
        playview.p1hp = 10
        playview.p2hp = 0
        playdata = Mock()
        playview.playdata = playdata

        with patch("card_common.Play_view", return_value=playview):
            judge(sid)
            playdata.gamewin.assert_called_once_with(sid)

        # Test case 3: Player 1 HP > 0 and Player 2 HP > 0
        sid = 1
        playview = Mock()
        playview.p1hp = 10
        playview.p2hp = 10
        playdata = Mock()
        playview.playdata = playdata

        with patch("card_common.Play_view", return_value=playview):
            judge(sid)
            playdata.gameover.assert_not_called()
            playdata.gamewin.assert_not_called()


# メイン関数
if __name__ == "__main__":
    unittest.main()
