import unittest
from unittest.mock import MagicMock, Mock, patch

import api_common_util
import card_db
from api_common_status import (
    api_common_active,
    api_common_attack,
    api_common_attack_card,
)


class TestAPICommonActive(unittest.TestCase):
    def test_api_common_active(self):
        # テスト用のダミー引数を設定
        sid = 1
        playview = Mock()
        effect = "active"
        card2 = "dummy_card"
        isRun = True

        # 子関数のMock化
        api_common_util.getobjcard = MagicMock()
        api_common_util.get_self_or_enemy = MagicMock(
            return_value=[None, None, None, None]
        )
        card_db.putsession = MagicMock()

        # 事前チェックは不要の場合のテスト
        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_active(sid, playview, effect, card2, False)
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            # card_db.putsessionが呼ばれていない事をチェック
            mock_putsession.assert_not_called()

        # 事前チェックが必要な場合のテスト

        # 自分自身をactive化するパターン
        effect = "onplay:self_active"
        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_active(sid, playview, effect, card2, isRun)
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once()

        # "active"以外のeffectの場合のテスト
        effect = "other_effect"
        with self.assertRaises(Exception):
            api_common_active(sid, playview, effect, card2, isRun)

    def test_api_common_attack_card(self):
        # Test case 1: Test with valid input
        sid = 1
        playview = Mock()
        effect = "self_attack+1"
        objcard2 = Mock()
        objcard2.dattack = 3

        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_attack_card(
                sid, playview, effect, objcard2
            )
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            mock_putsession.assert_called_once_with(
                playview.playdata.card_table, "cuid", objcard2.cuid, "dattack", 4
            )

        # Test case 2: Test with invalid input
        sid = 1
        playview = Mock()
        effect = "self_attack+1"
        objcard2 = None

        result, status_code = api_common_attack_card(sid, playview, effect, objcard2)
        self.assertEqual(result, {"error": "unit don't exists in target card"})
        self.assertEqual(status_code, 403)

        # このターンだけ攻撃力を上げるパターン
        sid = 1
        playview = Mock()
        effect = "unit_attack+2_thisturn"
        objcard2 = Mock()
        objcard2.dattack = 3
        card_db.getrecord_fromsession = Mock(
            return_value=[0, 0, 0, 0, 0, 0, 0, 0, "test"]
        )

        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_attack_card(
                sid, playview, effect, objcard2
            )
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            mock_putsession.assert_any_call(
                playview.playdata.card_table, "cuid", objcard2.cuid, "dattack", 5
            )
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "turnend_effect_ontime",
                "test,attack-2",
            )

        # 攻撃力をテンションから取得するパターン
        sid = 1
        playview = Mock()
        effect = "unit_attack+T_thisturn"
        objcard2 = Mock()
        objcard2.dattack = 0
        player_self = Mock()
        player_self.tension = 3
        api_common_util.get_self_or_enemy = Mock(
            return_value=[None, None, player_self, None]
        )

        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_attack_card(
                sid, playview, effect, objcard2
            )
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            mock_putsession.assert_any_call(
                playview.playdata.card_table, "cuid", objcard2.cuid, "dattack", 3
            )
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "turnend_effect_ontime",
                "test,attack-3",
            )

    def test_api_common_attack(self):
        # Test case 1: Test with valid input
        sid = 1
        objcard2 = Mock()
        objcard2.name = "test"
        objcard2.dattack = 3
        objcard2.cuid = "test_cuid"
        playview = Mock()
        playview.p1board = [None, None, None, objcard2]
        effect = "unit_attack+2"
        card2 = "leftboard_3"

        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_attack(sid, playview, effect, card2, True)
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            mock_putsession.assert_called_once_with(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dattack",
                5,
            )

        # Test case 2: Test with invalid input
        sid = 1
        playview = Mock()
        effect = "self_attack+1"
        card2 = ""

        result, status_code = api_common_attack(sid, playview, effect, card2, True)
        self.assertEqual(result, {"error": "unit don't exists in target card"})
        self.assertEqual(status_code, 403)

        # Test case 3: Test with non-existent unit
        sid = 1
        playview = Mock()
        playview.p1board = [None, None, None, None]
        effect = "self_attack+1"
        card2 = "leftboard_3"

        result, status_code = api_common_attack(sid, playview, effect, card2, True)
        self.assertEqual(result, {"error": "unit don't exists in target card"})
        self.assertEqual(status_code, 403)


if __name__ == "__main__":
    unittest.main()
