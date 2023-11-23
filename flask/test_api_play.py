import unittest
from unittest.mock import MagicMock, Mock, patch

from api_play import api_play_hand


class TestAPIPlay(unittest.TestCase):
    def test_api_play_hand(self):
        sid = 1
        objcard1 = Mock()
        objcard1.cost = 3
        objcard1.effect = "onplay:dummy_effect"
        objcard1.name = "card1"
        playview = Mock()
        playview.p1hand = [objcard1]
        playview.p1board = [None, None, None, None, None, None]
        playview.p1mp = 5
        playview.p1name = "p1"
        playview.p1hp = 10
        playview.p2hp = 10
        card1 = "card_0"
        card2 = "leftboard_3"
        card3 = ""

        with patch("api_play.Play_view") as mock_playview, patch(
            "api_common_common.apply_effect"
        ) as mock_apply_effect, patch("card_db.appendlog") as mock_appendlog, patch(
            "card_db.putcardtable"
        ) as mock_putsession, patch(
            "card_db.putplayerstats"
        ) as mock_putplayerstats, patch(
            "card_common.judge"
        ) as mock_cardcommon_judge:
            mock_apply_effect.return_value = ("OK", 200)

            # Test case 1: Test with valid input
            mock_playview.return_value = playview
            result = api_play_hand(sid, playview, card1, card2, card3)
            self.assertEqual(result, {"info": "OK"})
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                playview.p1hand[0].cuid,
                "loc",
                "p1_board",
            )
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                playview.p1hand[0].cuid,
                "locnum",
                3,
            )
            mock_putplayerstats.assert_any_call("name", playview.p1name, "mp", 2)

            # Test case 2: Test with invalid input
            sid = 1
            playview = Mock()
            playview.p1hand = [None]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""

            result = api_play_hand(sid, playview, card1, card2, card3)
            self.assertEqual(result, {"error": "illegal card1 number"})

            # Test case 3: Test with unit already exists in card2
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, Mock(), None, None]
            playview.p1mp = 5
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""

            result = api_play_hand(sid, playview, card1, card2, card3)
            self.assertEqual(result, {"error": "unit exists in card2"})

            # Test case 4: Test with insufficient MP
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 1
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""

            result = api_play_hand(sid, playview, card1, card2, card3)
            self.assertEqual(result, {"error": "MP short"})

            # Test case 5: Test with onplay effect that returns an error
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            playview.p1name = "test"
            playview.playdata.card_table = "test_table"
            playview.p1hp = 10
            playview.p2hp = 10
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""
            apply_effect = MagicMock(return_value=("error", 403))

            with patch("api_common_common.apply_effect", apply_effect):
                result = api_play_hand(sid, playview, card1, card2, card3)
                self.assertEqual(result, ("error", 403))

            # Test case 6: Test with onplay effect that returns OK
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            playview.p1name = "test"
            playview.playdata.card_table = "test_table"
            playview.p1hp = 10
            playview.p2hp = 10
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""
            apply_effect = MagicMock(return_value=("OK", 200))

            with patch("api_common_common.apply_effect", apply_effect):
                result = api_play_hand(sid, playview, card1, card2, card3)
                self.assertEqual(result, {"info": "OK"})

            # Test case 7: Test with player 1 HP <= 0
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            playview.p1name = "test"
            playview.playdata.card_table = "test_table"
            playview.p1hp = 0
            playview.p2hp = 10
            mock_playview.return_value = playview
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""

            with patch("card_db.appendlog"), patch("card_db.putcardtable"), patch(
                "card_common.judge"
            ) as mock_cardcommon_judge:
                result = api_play_hand(sid, playview, card1, card2, card3)
                self.assertEqual(result, {"info": "OK"})
                mock_cardcommon_judge.assert_called_once()

            # Test case 8: Test with player 2 HP <= 0
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            playview.p1name = "test"
            playview.playdata.card_table = "test_table"
            playview.p1hp = 10
            playview.p2hp = 0
            mock_playview.return_value = playview
            card1 = "card_0"
            card2 = "leftboard_3"
            card3 = ""

            with patch("card_db.appendlog"), patch("card_db.putcardtable"), patch(
                "card_common.judge"
            ) as mock_cardcommon_judge:
                result = api_play_hand(sid, playview, card1, card2, card3)
                self.assertEqual(result, {"info": "OK"})
                mock_cardcommon_judge.assert_called_once()

            # Test case 9: Test with illegal card2
            sid = 1
            playview = Mock()
            playview.p1hand = [objcard1]
            playview.p1board = [None, None, None, None, None, None]
            playview.p1mp = 5
            playview.p1name = "test"
            playview.playdata.card_table = "test_table"
            playview.p1hp = 10
            playview.p2hp = 10
            card1 = "card_0"
            card2 = "invalid_card2"
            card3 = ""

            result = api_play_hand(sid, playview, card1, card2, card3)
            self.assertEqual(result, ({"error": "illegal card2"}, 403))


# メイン関数
if __name__ == "__main__":
    unittest.main()
