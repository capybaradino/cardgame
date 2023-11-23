import unittest
from unittest.mock import MagicMock, Mock, patch

import api_attack
import api_common_common
import api_common_util
import card_db


class TestSpecifiedCase1(unittest.TestCase):
    # def setUp(self):

    def test_attack_bothdead_ondead1dmg_random(self):
        # 盤面構築
        self.sid = "test_sid"
        self.card1 = "leftboard_1"
        self.card2 = "rightboard_1"
        objcard1 = Mock()
        objcard2 = Mock()
        objcard1.name = "test_card1"
        objcard2.name = "test_card2"
        objcard1.attack = 1
        objcard2.attack = 2
        objcard1.refresh = Mock()
        objcard2.refresh = Mock()
        objcard1.status = ""
        objcard2.status = ""
        objcard1.effect = ""
        objcard2.effect = "ondead:enemy_1dmg_random"  # おばけキャンドル
        objcard1.dhp = 0
        objcard2.dhp = 0
        objcard1.hp_org = 1
        objcard2.hp_org = 1
        self.playview = Mock()
        self.playview.p1board = [None, objcard1, None, None, None, None]
        self.playview.p2board = [None, objcard2, None, None, None, None]
        # プレイヤー情報
        self.playview.p1name = "test_player_1"
        self.playview.p2name = "test_player_2"
        self.playview.p1tension = 2
        self.playview.p1mp = 2
        self.playview.p1job = "wiz"
        self.playview.p1 = Mock()
        self.playview.p2hp = 10
        self.playview.p2.hp = 10
        self.playview.playdata = Mock()
        self.playview.playdata.card_table = "test_card_table"
        self.playview.playdata.player1 = Mock()
        self.playview.playdata.player1.name = "test_player_1"
        self.playview.playdata.p1_player_tid = "test_player_1"
        self.playview.playdata.p2_player_tid = "test_player_2"
        self.playview.p2.player_tid = "test_player_2"
        self.playview.p1.name = "test_player_1"
        self.playview.p2.name = "test_player_2"
        # Mock設定
        card_db.getrecord_fromsession = Mock()
        card_db.getrecord_fromsession.return_value = [0, 0, "test_cuid", 0, 0, 0, 1, 0]
        self.playview.isblocked = Mock()
        self.playview.isblocked.return_value = False
        card_db.appendlog = Mock()
        card_db.putcardtable = Mock()
        api_common_util.get_self_or_enemy = Mock()
        api_common_util.get_self_or_enemy.return_value = [
            None,
            self.playview.p1board,
            self.playview.p2,
            self.playview.p1,
        ]
        api_common_common.leader_hp_change = Mock()
        api_common_common.unit_hp_change = Mock()

        api_common_util.getobjcard = Mock()
        api_common_util.getobjcard.return_value = None

        ret, scode = api_attack.api_unit_attack(
            self.sid, self.playview, self.card1, self.card2
        )
        api_common_common.leader_hp_change.assert_called_once_with(self.playview.p1, 1)
        assert ret == {"info": "OK"}
        assert scode == 200


if __name__ == "__main__":
    unittest.main()
