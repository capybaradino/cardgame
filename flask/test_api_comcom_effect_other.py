import unittest
from unittest.mock import Mock, patch

import api_common_common
import api_common_status
import api_common_tension
import api_common_util
import card_db
from api_common_common import apply_effect


class TestApplyEffect_other(unittest.TestCase):
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

    def tearDown(self):
        # Mockオブジェクトのリセット
        self.mock_unit_hp_change_multi.reset_mock()
        self.mock_api_common_dmg.reset_mock()
        self.mock_api_common_dmg_leader.reset_mock()
        self.mock_api_common_attack.reset_mock()
        self.mock_api_common_active.reset_mock()
        self.mock_api_common_tension.reset_mock()
        self.mock_api_common_get_self_or_enemy.reset_mock()
        self.mock_getobjcard.reset_mock()

    # ドローのテスト
    @patch("api_common_common.unit_hp_change_multi", mock_unit_hp_change_multi)
    @patch("api_common_common.api_common_dmg", mock_api_common_dmg)
    @patch("api_common_common.api_common_dmg_leader", mock_api_common_dmg_leader)
    @patch("api_common_status.api_common_attack", mock_api_common_attack)
    @patch("api_common_status.api_common_active", mock_api_common_active)
    @patch("api_common_tension.api_common_tension", mock_api_common_tension)
    @patch("api_common_util.get_self_or_enemy", mock_api_common_get_self_or_enemy)
    @patch("api_common_util.getobjcard", mock_getobjcard)
    def test_apply_effect_draw(self):
        # draw_bujutsuのテスト
        effect = "self_1draw_bujutsu"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.playview.p1.draw_bujutsucard.assert_called_once()

        # draw_card_spellのテスト
        effect = "self_1draw_spell"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.playview.p1.draw_card_spell.assert_called_once()

    # attack等のテスト
    @patch("api_common_common.unit_hp_change_multi", mock_unit_hp_change_multi)
    @patch("api_common_common.api_common_dmg", mock_api_common_dmg)
    @patch("api_common_common.api_common_dmg_leader", mock_api_common_dmg_leader)
    @patch("api_common_status.api_common_attack", mock_api_common_attack)
    @patch("api_common_status.api_common_active", mock_api_common_active)
    @patch("api_common_tension.api_common_tension", mock_api_common_tension)
    @patch("api_common_util.get_self_or_enemy", mock_api_common_get_self_or_enemy)
    @patch("api_common_util.getobjcard", mock_getobjcard)
    def test_apply_effect_attack(self):
        # attackのテスト
        effect = "unit_attack+2_thisturn"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_attack.assert_called_once()

        # tensionのテスト
        effect = "tension+2"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_tension.assert_called_once()

        # activeのテスト
        effect = "active"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_active.assert_called_once()

        # 前回のテストで呼び出されたMockオブジェクトをリセット
        self.mock_api_common_dmg_leader.reset_mock()
        # dmgのテスト(対象が敵リーダー限定)
        effect = "enemy_3dmg_leader"
        card3 = "test_card3"
        result = apply_effect(
            self.sid, self.playview, effect, None, self.card2, card3, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが期待通りに呼び出されたことを確認
        self.mock_api_common_dmg_leader.assert_called_once()

    # movefrontのテスト
    @patch("api_common_common.unit_hp_change_multi", mock_unit_hp_change_multi)
    @patch("api_common_common.api_common_dmg", mock_api_common_dmg)
    @patch("api_common_common.api_common_dmg_leader", mock_api_common_dmg_leader)
    @patch("api_common_status.api_common_attack", mock_api_common_attack)
    @patch("api_common_status.api_common_active", mock_api_common_active)
    @patch("api_common_tension.api_common_tension", mock_api_common_tension)
    @patch("api_common_util.get_self_or_enemy", mock_api_common_get_self_or_enemy)
    @patch("api_common_util.getobjcard", mock_getobjcard)
    def test_apply_effect_movefront(self):
        effect = "onplay:allbackunit_movefront"
        # 対象無し
        board_enemy = [None, None, None, None, None, None]
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [None, board_enemy, None, None]
        api_common_util.getobjcard_oppsite = Mock()
        api_common_util.getobjcard_oppsite.return_value = [None, 0, 1]
        card_db.putdeck_locnum = Mock()
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが呼び出されなかったことを確認
        api_common_util.getobjcard_oppsite.assert_not_called()

        # 対象無し(前列にユニットが存在する)
        board_enemy = [Mock(), Mock(), Mock(), None, Mock(), None]
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [None, board_enemy, None, None]
        api_common_util.getobjcard_oppsite = Mock()
        card_db.putdeck_locnum = Mock()
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが呼び出されなかったことを確認
        api_common_util.getobjcard_oppsite.assert_not_called()

        # 対象あり
        board_enemy = [None, None, None, None, Mock(), Mock()]
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [None, board_enemy, None, None]
        api_common_util.getobjcard_oppsite = Mock()
        card_db.putdeck_locnum = Mock()
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが2回呼び出されたことを確認
        self.assertEqual(card_db.putdeck_locnum.call_count, 2)

        # 対象あり(前列あり無し混在)
        # Mockオブジェクトをリセット
        card_db.putdeck_locnum.reset_mock()
        board_enemy = [Mock(), Mock(), None, None, Mock(), Mock()]
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [None, board_enemy, None, None]
        api_common_util.getobjcard_oppsite = Mock()
        card_db.putdeck_locnum = Mock()
        result = apply_effect(
            self.sid, self.playview, effect, self.objcard3, self.card2, None, self.isRun
        )
        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))
        # Mockオブジェクトが1回呼び出されたことを確認
        self.assertEqual(card_db.putdeck_locnum.call_count, 1)


if __name__ == "__main__":
    unittest.main()
