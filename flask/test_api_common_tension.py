import unittest
from unittest.mock import MagicMock, Mock, patch

import api_common_tension
import api_common_util
import card_db
from api_spell import api_spell


class TestAPICommonTension(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.objcard2 = Mock()
        self.objcard2.cuid = "test_cuid"
        self.objcard2.name = "test_name"
        self.objcard2.status = ""
        self.objcard2.dhp = 5
        self.objcard2.dattack = 3
        self.objcard2.cuid = "test_cuid"
        self.playview = Mock()
        self.playview.p1name = "test_name"
        self.player_self = Mock()
        self.player_self.tension = 1
        self.player_self.player_tid = 1
        self.player_enemy = Mock()
        self.player_enemy.tension = 2
        self.player_enemy.player_tid = 2

    def tearDown(self):
        pass

    @patch("card_db.putplayerstats")
    def test_api_common_tension_objcard_with_self_tension_effect(self, mock_putsession):
        # Test case 1: Test with self_tension effect
        mock_putsession.return_value = None
        result, status_code = api_common_tension.api_common_tension_objcard(
            self.sid,
            self.playview,
            "self_tension+1",
            self.objcard2,
            True,
            self.player_self,
            self.player_enemy,
        )
        self.assertEqual(result, "OK")
        self.assertEqual(status_code, 200)
        mock_putsession.assert_called_once_with(
            "player_tid", self.player_self.player_tid, "tension", 2
        )

    @patch("card_db.putplayerstats")
    def test_api_common_tension_objcard_with_enemy_tension_effect(
        self, mock_putsession
    ):
        # Test case 2: Test with enemy_tension effect
        mock_putsession.return_value = None
        result, status_code = api_common_tension.api_common_tension_objcard(
            self.sid,
            self.playview,
            "enemy_tension-1",
            self.objcard2,
            True,
            self.player_self,
            self.player_enemy,
        )
        self.assertEqual(result, "OK")
        self.assertEqual(status_code, 200)
        mock_putsession.assert_called_once_with(
            "player_tid", self.player_enemy.player_tid, "tension", 1
        )

    @patch("card_db.putplayerstats")
    def test_api_common_tension_objcard_with_each_tension_effect(self, mock_putsession):
        # Test case 3: Test with each_tension effect
        mock_putsession.return_value = None
        result, status_code = api_common_tension.api_common_tension_objcard(
            self.sid,
            self.playview,
            "each_tension+3",
            self.objcard2,
            True,
            self.player_self,
            self.player_enemy,
        )
        self.assertEqual(result, "OK")
        self.assertEqual(status_code, 200)
        mock_putsession.assert_any_call(
            "player_tid", self.player_self.player_tid, "tension", 3
        )
        mock_putsession.assert_any_call(
            "player_tid", self.player_enemy.player_tid, "tension", 3
        )

    @patch("card_db.putcardtable")
    def test_api_common_tension_objcard_with_invalid_effect(self, mock_putsession):
        # Test case 4: Test with invalid effect
        mock_putsession.return_value = None
        with self.assertRaises(Exception):
            api_common_tension.api_common_tension_objcard(
                self.sid,
                self.playview,
                "invalid_effect",
                self.objcard2,
                True,
                self.player_self,
                self.player_enemy,
            )


# メイン処理
if __name__ == "__main__":
    unittest.main()
