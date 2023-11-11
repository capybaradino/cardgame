import unittest
from unittest.mock import Mock, patch

import api_common_util
import card_db
from api_attack import api_onattack, api_unit_attack


class TestAPIUnitAttack(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.playview = Mock()
        self.card1 = "leftboard_0"
        self.card2 = "rightboard_3"
        self.pattern_p2board = r"rightboard_[0-5]$"
        self.pattern_p2leader = r"rightboard_10"
        self.objcard1 = Mock()
        self.objcard1.cuid = "test_cuid_1"
        self.objcard1.name = "test_card_1"
        self.objcard1.attack = 3
        self.objcard2 = Mock()
        self.objcard2.cuid = "test_cuid_2"
        self.objcard2.name = "test_card_2"
        self.objcard2.attack = 2
        self.objcard2.status = []
        self.playview.p1board = [self.objcard1, None, None, None]
        self.playview.p2board = [None, None, None, self.objcard2]
        self.playview.p1name = "test_player_1"
        self.playview.p2name = "test_player_2"
        self.playview.p2hp = 10
        self.playview.playdata = Mock()
        self.playview.playdata.card_table = "test_card_table"
        self.playview.playdata.player1 = Mock()
        self.playview.playdata.player1.name = "test_player_1"
        self.playview.playdata.p1_player_tid = 1
        self.playview.playdata.p2_player_tid = 2
        card_db.getrecord_fromsession = Mock()
        card_db.getrecord_fromsession.return_value = [0, 0, 0, 0, 0, 0, 1, 0]
        card_db.appendlog = Mock()

    def test_api_unit_attack_with_valid_input(self):
        with patch(
            "card_db.getrecord_fromsession"
        ) as mock_getrecord_fromsession, patch(
            "card_db.appendlog"
        ) as mock_appendlog, patch(
            "card_db.putsession"
        ) as mock_putsession, patch(
            "api_attack.api_onattack"
        ) as mock_api_onattack, patch(
            "api_common_common.unit_hp_change_multi"
        ) as mock_unit_hp_change_multi:
            mock_api_onattack.return_value = "OK", 200
            mock_unit_hp_change_multi.return_value = "OK", 200
            self.playview.isblocked = Mock()
            self.playview.isblocked.return_value = False
            result, status_code = api_unit_attack(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            mock_getrecord_fromsession.assert_called_once_with(
                self.playview.playdata.card_table, "cuid", self.objcard1.cuid
            )
            mock_appendlog.assert_any_call(
                self.playview.playdata.card_table,
                "[" + self.playview.p1name + "]attack:" + self.objcard1.name,
            )
            mock_appendlog.assert_any_call(
                self.playview.playdata.card_table, "target->" + self.objcard2.name
            )
            mock_putsession.assert_called_with(
                self.playview.playdata.card_table,
                "cuid",
                self.objcard1.cuid,
                "active",
                0,
            )
            mock_unit_hp_change_multi.assert_called_with(
                self.sid,
                self.playview,
                [self.objcard2, self.objcard1],
                [self.objcard1.attack, self.objcard2.attack],
            )
            mock_api_onattack.assert_called_with(self.sid, self.playview, self.objcard1)

    def test_api_unit_attack_with_invalid_card1(self):
        self.playview.p1board[0] = None
        result, status_code = api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        self.assertEqual(result, {"error": "illegal card1 number"})
        self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_inactive_card1(self):
        with patch("card_db.getrecord_fromsession") as mock_getrecord_fromsession:
            mock_getrecord_fromsession.return_value = [0, 0, 0, 0, 0, 0, 0, 0]
            result, status_code = api_unit_attack(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"error": "card1 is not active"})
            self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_invalid_card2(self):
        self.card2 = "invalid_card"
        result, status_code = api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        self.assertEqual(result, {"error": "illegal card2"})
        self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_blocked_card2(self):
        self.playview.isblocked = Mock()
        self.playview.isblocked.return_value = True
        result, status_code = api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        self.assertEqual(result, {"error": "card2 is blocked by other unit"})
        self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_stealth_card2(self):
        self.playview.isblocked = Mock()
        self.playview.isblocked.return_value = False
        self.objcard2.status = ["stealth"]
        result, status_code = api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        self.assertEqual(result, {"error": "card2 has stealth"})
        self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_wall(self):
        self.playview.iswall = Mock()
        self.playview.iswall.return_value = True
        self.card2 = self.pattern_p2leader
        result, status_code = api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        self.assertEqual(result, {"error": "wall exists"})
        self.assertEqual(status_code, 403)

    def test_api_unit_attack_with_leader(self):
        self.card2 = self.pattern_p2leader
        with patch("card_db.putsession") as mock_putsession, patch(
            "api_attack.api_onattack"
        ) as mock_api_onattack:
            mock_api_onattack.return_value = "OK", 200
            self.playview.iswall = Mock()
            self.playview.iswall.return_value = False
            result, status_code = api_unit_attack(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            mock_putsession.assert_any_call(
                "playerstats",
                "player_tid",
                self.playview.playdata.p2_player_tid,
                "hp",
                7,
            )
            mock_api_onattack.assert_called_with(
                self.sid, self.playview, self.objcard1, ifleader=True
            )


class TestAPIOnAttack(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.playview = Mock()
        self.objcard1 = Mock()
        self.objcard1.cuid = "test_cuid_1"
        self.objcard1.name = "test_card_1"
        self.objcard1.attack = 3
        self.objcard1.status = ""
        self.objcard1.effect = ""
        self.objcard2 = Mock()
        self.objcard2.cuid = "test_cuid_2"
        self.objcard2.name = "test_card_2"
        self.objcard2.attack = 2
        self.objcard2.status = []
        self.playview.p1board = [self.objcard1, None, None, None]
        self.playview.p2board = [None, None, None, self.objcard2]
        self.playview.p1name = "test_player_1"
        self.playview.p2name = "test_player_2"
        self.playview.p2hp = 10
        self.playview.playdata = Mock()
        self.playview.playdata.card_table = "test_card_table"
        self.playview.playdata.player1 = Mock()
        self.playview.playdata.player1.name = "test_player_1"
        self.playview.playdata.p1_player_tid = 1
        self.playview.playdata.p2_player_tid = 2
        card_db.getrecord_fromsession = Mock()
        card_db.getrecord_fromsession.return_value = [0, 0, 0, 0, 0, 0, 1, 0]
        card_db.appendlog = Mock()
        card_db.putsession = Mock()
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [
            Mock(),
            Mock(),
            self.playview.p1player,
            self.playview.p2player,
        ]

    def test_api_onattack_with_attack_subeffect(self):
        with patch(
            "api_common_status.api_common_attack_card"
        ) as mock_api_common_attack_card:
            self.objcard1.effect = "onattack:self_attack+1"
            api_onattack(self.sid, self.playview, self.objcard1)
            mock_api_common_attack_card.assert_called_once_with(
                self.sid, self.playview, "self_attack+1", self.objcard1
            )

    def test_api_onattack_with_draw_subeffect_and_enemy(self):
        # 敵に1ドロー
        self.objcard1.effect = "onattack:enemy_1draw_any"
        api_onattack(self.sid, self.playview, self.objcard1)
        self.assertEqual(self.playview.p2player.draw_card.call_count, 1)

    # def test_api_onattack_with_draw_subeffect_and_self(self):
    #     # 自分に1ドロー
    #     self.objcard1.effect = "onattack:self_1draw"
    #     api_onattack(self.sid, self.playview, self.objcard1)
    #     self.assertEqual(self.playview.p1player.draw_card.call_count, 1)

    def test_api_onattack_leader_draw_bujutsu(self):
        # 攻撃対象が敵リーダーだった場合、武術カードを1ドロー
        self.objcard1.effect = "onattack_leader:self_1draw_bujutsu"
        api_onattack(self.sid, self.playview, self.objcard1, ifleader=True)
        self.assertEqual(self.playview.p1player.draw_bujutsucard.call_count, 1)

    def test_api_onattack_leader_draw_bujutsu(self):
        # 攻撃対象が敵リーダーじゃなかった場合、武術カードを1ドローしない
        self.objcard1.effect = "onattack_leader:self_1draw_bujutsu"
        api_onattack(self.sid, self.playview, self.objcard1)
        self.assertEqual(self.playview.p1player.draw_bujutsucard.call_count, 0)

    def test_api_onattack_with_stealth_status(self):
        # ステルス解除
        self.objcard1.status = ",stealth"
        api_onattack(self.sid, self.playview, self.objcard1)
        card_db.putsession.assert_called_once_with(
            self.playview.playdata.card_table, "cuid", self.objcard1.cuid, "status", ""
        )


# メイン関数
if __name__ == "__main__":
    unittest.main()
