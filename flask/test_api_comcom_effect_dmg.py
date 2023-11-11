import unittest
from unittest.mock import Mock, patch

import api_common_common
import api_common_status
import api_common_tension
import api_common_util
from api_common_common import apply_effect


class TestApplyEffect_dmg(unittest.TestCase):
    mock_unit_hp_change_multi = Mock()
    mock_api_common_dmg = Mock()
    mock_api_common_dmg_leader = Mock()
    mock_api_common_attack = Mock()
    mock_api_common_active = Mock()
    mock_api_common_tension = Mock()
    mock_api_common_get_self_or_enemy = Mock()
    mock_getobjcard = Mock()

    def setUp(self):
        # Mockオブジェクトの設定
        self.objcard3 = Mock()
        self.objcard3.status = "test_status"
        self.mock_getobjcard.return_value = self.objcard3
        self.mock_api_common_dmg.return_value = ("OK", 200)
        self.mock_api_common_dmg_leader.return_value = ("OK", 200)
        self.mock_api_common_active.return_value = ("OK", 200)
        self.mock_api_common_attack.return_value = ("OK", 200)
        self.mock_api_common_tension.return_value = ("OK", 200)
        self.mock_api_common_get_self_or_enemy.return_value = [
            Mock(),
            Mock(),
            Mock(),
            Mock(),
        ]
        self.sid = "test_sid"
        self.playview = Mock()  # Play_viewのMockオブジェクト
        self.playview.p1 = Mock()
        self.playview.p1.draw_bujutsucard = Mock()
        self.playview.p1.draw_card_spell = Mock()
        self.playview.p1.draw_card = Mock()
        self.card2 = "test_card2"
        self.isRun = True

    @patch("api_common_common.unit_hp_change_multi", mock_unit_hp_change_multi)
    @patch("api_common_common.api_common_dmg", mock_api_common_dmg)
    @patch("api_common_common.api_common_dmg_leader", mock_api_common_dmg_leader)
    @patch("api_common_status.api_common_attack", mock_api_common_attack)
    @patch("api_common_status.api_common_active", mock_api_common_active)
    @patch("api_common_tension.api_common_tension", mock_api_common_tension)
    @patch("api_common_util.get_self_or_enemy", mock_api_common_get_self_or_enemy)
    @patch("api_common_util.getobjcard", mock_getobjcard)
    def test_apply_effect_dmg(self):
        # dmgのテスト
        effect = "any_5dmg"
        card3 = "rightboard_3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_dmg.assert_called_once()

        # dmgのテスト(対象が敵リーダー)
        effect = "enemy_5dmg"
        card3 = "rightboard_10"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_dmg_leader.assert_called_once()

        # dmgのテスト(前列指定(OK))
        effect = "unit_5dmg_frontonly"
        card3 = "rightboard_1"
        self.objcard3.locnum = 1
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))

        # dmgのテスト(前列指定(NG))
        effect = "unit_5dmg_frontonly"
        card3 = "rightboard_3"
        self.objcard3.locnum = 3
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ({"error": "target unit is not front"}, 403))

        # dmgのテスト(ユニット限定でリーダー指定)
        effect = "unit_5dmg"
        card3 = "rightboard_10"
        self.objcard3.locnum = 10
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ({"error": "cannot target leader"}, 403))

        # dmgのテスト(縦一列指定)
        effect = "enemy_vertical_4dmg_frontonly"
        card3 = "rightboard_1"
        self.objcard3.locnum = 1
        self.playview.p2board = [None, self.objcard3, None, None, None, None]
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認(OK)
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_unit_hp_change_multi.assert_called_once()

        # dmgのテスト(敵３体以上なら敵全ユニットにダメージ)
        # Mockオブジェクトをリセット
        self.mock_unit_hp_change_multi.reset_mock()
        effect = "onplay_enemy_unit_3over:all_enemy_unit_1dmg"
        objcard_enemy1 = Mock()
        objcard_enemy1.hp_org = 5
        objcard_enemy1.dhp = 0
        objcard_enemy2 = Mock()
        objcard_enemy2.hp_org = 5
        objcard_enemy2.dhp = 0
        objcard_enemy3 = Mock()
        objcard_enemy3.hp_org = 5
        objcard_enemy3.dhp = 0
        self.playview.p2board = [
            None,
            objcard_enemy1,
            None,
            None,
            objcard_enemy2,
            objcard_enemy3,
        ]
        self.mock_api_common_get_self_or_enemy.return_value = [
            None,
            self.playview.p2board,
            None,
            None,
        ]
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認(OK)
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_unit_hp_change_multi.assert_called_once()

        # dmgのテスト(敵が３体未満の場合hp_changeは実行されない)
        # Mockオブジェクトをリセット
        self.mock_unit_hp_change_multi.reset_mock()
        effect = "onplay_enemy_unit_3over:all_enemy_unit_1dmg"
        self.playview.p2board = [None, objcard_enemy1, None, None, None, None]
        self.mock_api_common_get_self_or_enemy.return_value = [
            None,
            self.playview.p2board,
            None,
            None,
        ]
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認(OK)
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが呼び出されなかったことを確認
        self.mock_unit_hp_change_multi.assert_not_called()

        # dmgのテスト(対象が敵リーダー限定)
        # 前回のテストで呼び出されたMockオブジェクトをリセット
        self.mock_api_common_dmg_leader.reset_mock()
        effect = "enemy_3dmg_leader"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_dmg_leader.assert_called_once()


if __name__ == "__main__":
    unittest.main()
