import unittest
from unittest.mock import Mock, patch

import api_common_common
import api_common_util
import api_tension
import card_db


class TestAPITension(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.playview = Mock()
        self.playview.p1name = "test_player_1"
        self.playview.p2name = "test_player_2"
        self.playview.p1tension = 2
        self.playview.p1mp = 2
        self.playview.p1job = "wiz"
        self.playview.p2board = [None, None, None, None]
        self.playview.p2hp = 10
        self.playview.p2.hp = 10
        self.playview.playdata = Mock()
        self.playview.playdata.card_table = "test_card_table"
        self.playview.playdata.player1 = Mock()
        self.playview.playdata.player1.name = "test_player_1"
        self.playview.playdata.p1_player_tid = "test_player_1"
        self.playview.playdata.p2_player_tid = "test_player_2"
        self.playview.p2.player_tid = "test_player_2"
        card_db.getrecord_fromsession = Mock()
        card_db.getrecord_fromsession.return_value = [0, 0, "test_cuid", 0, 0, 0, 1, 0]
        card_db.putsession = Mock()
        card_db.appendlog = Mock()
        api_common_common.unit_hp_change = Mock()

    def test_api_tension_with_tension_up(self):
        result = api_tension.api_tension(self.sid, self.playview, "card1", "card2")
        self.assertEqual(result, {"info": "OK"})
        card_db.putsession.assert_any_call(
            "playerstats", "name", self.playview.p1name, "mp", 1
        )
        card_db.putsession.assert_any_call(
            "playerstats", "name", self.playview.p1name, "tension", 3
        )
        card_db.putsession.assert_any_call(
            self.playview.playdata.card_table, "cuid", "test_cuid", "active", 0
        )
        card_db.appendlog.assert_called_once_with(
            self.playview.playdata.card_table,
            "[" + self.playview.p1name + "]tension up:",
        )

    def test_api_tension_with_tension_up_not_active(self):
        card_db.getrecord_fromsession.return_value = [0, 0, "test_cuid", 0, 0, 0, 0, 0]
        result = api_tension.api_tension(self.sid, self.playview, "card1", "card2")
        self.assertEqual(result, {"error": "Tension not active"})

    def test_api_tension_with_tension_up_mp_short(self):
        self.playview.p1mp = 0
        result = api_tension.api_tension(self.sid, self.playview, "card1", "card2")
        self.assertEqual(result, {"error": "MP short"})

    def test_api_tension_with_tension_skill_wiz_board(self):
        self.playview.p1tension = 3
        objcard2 = Mock()
        objcard2.refresh = Mock()
        objcard2.status = "test_status"
        objcard2.name = "test_name"
        api_common_util.getobjcard = Mock()
        api_common_util.getobjcard.return_value = objcard2
        self.playview.p2board[0] = objcard2
        result = api_tension.api_tension(
            self.sid, self.playview, "card1", "rightboard_0"
        )
        self.assertEqual(result, {"info": "OK"})
        api_common_common.unit_hp_change.assert_called_once_with(
            self.sid, self.playview, self.playview.p2board[0], 3
        )
        card_db.appendlog.assert_any_call(
            self.playview.playdata.card_table,
            "[" + self.playview.p1name + "]tension skill:",
        )
        card_db.appendlog.assert_any_call(
            self.playview.playdata.card_table,
            "effect->" + self.playview.p2board[0].name,
        )

    def test_api_tension_with_tension_skill_wiz_leader(self):
        self.playview.p1tension = 3
        api_common_common.leader_hp_change = Mock()
        result = api_tension.api_tension(
            self.sid, self.playview, "card1", "rightboard_10"
        )
        self.assertEqual(result, {"info": "OK"})
        # card_db.putsession.assert_any_call(
        #     "playerstats",
        #     "player_tid",
        #     self.playview.p2.player_tid,
        #     "hp",
        #     7,
        # )
        api_common_common.leader_hp_change.assert_called_once_with(self.playview.p2, 3)
        card_db.appendlog.assert_any_call(
            self.playview.playdata.card_table,
            "[" + self.playview.p1name + "]tension skill:",
        )
        card_db.appendlog.assert_any_call(
            self.playview.playdata.card_table, "effect->" + self.playview.p2name
        )

    def test_api_tension_with_tension_skill_wiz_illegal_card2(self):
        self.playview.p1tension = 3
        result = api_tension.api_tension(
            self.sid, self.playview, "card1", "invalid_card"
        )
        self.assertEqual(result, ({"error": "illegal target"}, 403))

    def test_api_tension_with_tension_skill_wiz_unit_dont_exist(self):
        self.playview.p1tension = 3
        api_common_util.getobjcard = Mock()
        api_common_util.getobjcard.return_value = None
        result = api_tension.api_tension(
            self.sid, self.playview, "card1", "rightboard_0"
        )
        self.assertEqual(result, ({"error": "unit don't exists in target"}, 403))

    def test_api_tension_with_tension_skill_wiz_antieffect(self):
        self.playview.p1tension = 3
        objcard2 = Mock()
        objcard2.refresh = Mock()
        objcard2.status = "antieffect"
        objcard2.name = "test_name"
        api_common_util.getobjcard = Mock()
        api_common_util.getobjcard.return_value = objcard2
        result = api_tension.api_tension(
            self.sid, self.playview, "card1", "rightboard_0"
        )
        self.assertEqual(result, ({"error": "target unit has antieffect"}, 403))

    def test_api_tension_with_tension_skill_mnk(self):
        self.playview.p1tension = 3
        self.playview.p1job = "mnk"
        result = api_tension.api_tension(self.sid, self.playview, "card1", "card2")
        self.assertEqual(result, {"info": "OK"})
        self.assertEqual(self.playview.p1.draw_card.call_count, 1)
        self.assertEqual(self.playview.p1.draw_bujutsucard.call_count, 1)
        card_db.appendlog.assert_called_once_with(
            self.playview.playdata.card_table,
            "[" + self.playview.p1name + "]tension skill:",
        )

    def test_api_tension_with_tension_skill_unknown_job(self):
        self.playview.p1tension = 3
        self.playview.p1job = "unknown_job"
        result = api_tension.api_tension(self.sid, self.playview, "card1", "card2")
        self.assertEqual(result, ({"error": "unknown job"}, 403))


# メイン関数
if __name__ == "__main__":
    unittest.main()
