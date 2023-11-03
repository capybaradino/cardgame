import unittest
from unittest.mock import MagicMock, Mock, patch

import api_common_common
import api_common_util
import card_db
from api_spell import api_spell


class TestAPISpell(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.objcard = Mock()
        self.objcard.effect = "any_3dmg"
        self.objcard.cost = 3
        self.objcard.name = "test_name"
        self.playview = Mock()
        self.playview.p1hand = [None, self.objcard]
        self.playview.p1mp = 5
        self.playview.p1name = "test_name"
        self.playview.playdata.card_table = "test_card_table"
        self.card1 = "card1_1"
        self.card2 = "leftboard_1"
        self.objcard1 = Mock()
        self.objcard1.effect = "self_1drow,switch,dmg_enemy_1"
        self.objcard1.cost = 3
        self.objcard1.status = ""
        self.objcard1.name = "test_name"
        self.objcard2 = Mock()
        self.objcard2.cuid = "test_cuid"
        self.objcard2.name = "test_name"
        self.objcard2.status = ""
        self.objcard2.dhp = 5
        self.objcard2.dattack = 3
        self.objcard2.cuid = "test_cuid"
        self.objcard3 = Mock()
        self.objcard3.cuid = "test_cuid_2"
        self.objcard3.name = "test_name_2"
        self.objcard3.status = ""
        self.objcard3.dhp = 5
        self.objcard3.dattack = 3
        self.objcard3.cuid = "test_cuid_2"
        self.pattern_p1board = r"leftboard_[0-5]$"
        self.pattern_p2board = r"rightboard_[0-5]$"
        self.pattern_p1leader = r"leftboard_10"
        self.pattern_p2leader = r"rightboard_10"
        card_db.appendlog = Mock()

    def test_api_spell_with_illegal_card1_number(self):
        # Test case 1: Test with illegal card1 number
        api_common_util.getobjcard = MagicMock(return_value=None)
        result, status_code = api_spell(self.sid, self.playview, "card_0", self.card2)
        self.assertEqual(result, {"error": "illegal card1 number"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_self_1drow_effect(self):
        # Test case 2: Test with self_1drow effect
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        card_db.putsession = MagicMock()
        self.objcard.effect = "self_1drow"
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"info": "OK"})
        self.assertEqual(status_code, 200)
        card_db.putsession.assert_any_call(
            "playerstats", "name", self.playview.p1name, "mp", 2
        )
        card_db.putsession.assert_any_call(
            self.playview.playdata.card_table,
            "cuid",
            self.objcard.cuid,
            "loc",
            self.playview.p1name + "_cemetery",
        )

    def test_api_spell_with_switch_effect(self):
        # Test case 3: Test with switch effect
        api_common_util.getobjcard = MagicMock(return_value=self.objcard2)
        api_common_util.getobjcard_oppsite = MagicMock(
            return_value=(self.objcard3, 2, 1)
        )
        card_db.putdeck_locnum = MagicMock()
        card_db.putsession = MagicMock()
        self.objcard.effect = "switch"
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"info": "OK"})
        self.assertEqual(status_code, 200)
        api_common_util.getobjcard_oppsite.assert_called_once_with(
            self.playview, self.card2
        )
        card_db.putdeck_locnum.assert_any_call(
            self.playview.playdata.card_table, self.objcard2.cuid, 1
        )
        card_db.putdeck_locnum.assert_any_call(
            self.playview.playdata.card_table, self.objcard3.cuid, 2
        )
        card_db.putsession.assert_any_call(
            "playerstats", "name", self.playview.p1name, "mp", 2
        )
        card_db.putsession.assert_any_call(
            self.playview.playdata.card_table,
            "cuid",
            self.objcard.cuid,
            "loc",
            self.playview.p1name + "_cemetery",
        )

    def test_api_spell_with_dmg_enemy_effect(self):
        # Test case 4: Test with dmg_enemy effect
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        card_db.putsession = MagicMock()
        api_common_common.unit_hp_change = MagicMock()
        self.objcard.effect = "any_3dmg"
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"info": "OK"})
        self.assertEqual(status_code, 200)
        api_common_common.unit_hp_change.assert_called_once_with(
            self.sid, self.playview, self.objcard1, 3
        )
        card_db.putsession.assert_any_call(
            "playerstats", "name", self.playview.p1name, "mp", 2
        )
        card_db.putsession.assert_any_call(
            self.playview.playdata.card_table,
            "cuid",
            self.objcard.cuid,
            "loc",
            self.playview.p1name + "_cemetery",
        )

    def test_api_spell_with_dmg_enemy_effect_and_antieffect(self):
        # Test case 5: Test with dmg_enemy effect and antieffect
        api_common_util.getobjcard = MagicMock(return_value=self.objcard2)
        self.objcard2.status = "antieffect"
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"error": "card2 has antieffect"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_illegal_card2(self):
        # Test case 6: Test with illegal card2
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        result, status_code = api_spell(
            self.sid, self.playview, self.card1, "dummy_card"
        )
        self.assertEqual(result, {"error": "illegal card2"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_illegal_card2_unit(self):
        # Test case 7: Test with illegal card2 unit
        api_common_util.getobjcard = MagicMock(return_value=None)
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"error": "unit don't exists in card2"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_mp_short(self):
        # Test case 8: Test with mp short
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        api_common_util.getobjcard_oppsite = MagicMock(return_value=self.objcard2)
        self.playview.p1mp = 2
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"error": "MP short"})
        self.assertEqual(status_code, 403)


if __name__ == "__main__":
    unittest.main()
