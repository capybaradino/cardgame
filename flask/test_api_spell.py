import unittest
from unittest.mock import MagicMock, Mock, patch

import api_common_common
import api_common_tension
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
        self.card2 = "rightboard_1"
        self.objcard1 = Mock()
        self.objcard1.effect = "self_1draw,switch,dmg_enemy_1"
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
        self.player_self = Mock()
        self.player_self.draw_card = Mock()
        self.player_enemy = Mock()
        self.player_enemy.draw_card = Mock()
        api_common_util.get_self_or_enemy = MagicMock(
            return_value=(Mock(), Mock(), self.player_self, self.player_enemy)
        )

    def test_api_spell_with_illegal_card1_number(self):
        # Test case 1: Test with illegal card1 number
        api_common_util.getobjcard = MagicMock(return_value=None)
        result, status_code = api_spell(self.sid, self.playview, "card_0", self.card2)
        self.assertEqual(result, {"error": "illegal card1 number"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_self_1draw_effect(self):
        # Test case 2: Test with self_1draw effect
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            playview_end.p1board = [None, None, None, None, None, None]
            play_view_mock.return_value = playview_end
            api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
            card_db.putsession = MagicMock()
            self.objcard.effect = "self_1draw"
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            self.player_self.draw_card.assert_called_once()
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
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            self.objcard2.effect = ""
            playview_end.p1board = [None, self.objcard2, None, None, None, None]
            play_view_mock.return_value = playview_end
            api_common_util.getobjcard = MagicMock(return_value=self.objcard2)
            api_common_util.getobjcard_oppsite = MagicMock(
                return_value=(self.objcard3, 2, 1)
            )
            card_db.putdeck_locnum = MagicMock()
            card_db.putsession = MagicMock()
            self.objcard.effect = "switch"
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
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
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            playview_end.p1board = [None, None, None, None, None, None]
            play_view_mock.return_value = playview_end
            api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
            card_db.putsession = MagicMock()
            api_common_common.unit_hp_change = MagicMock(return_value=3)
            self.objcard.effect = "any_3dmg"
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
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

    def test_api_spell_with_dmg_enemy_effect_3times(self):
        # Test case 4-2: Test with dmg_enemy effect 3times
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            playview_end.p1board = [None, None, None, None, None, None]
            play_view_mock.return_value = playview_end
            api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
            card_db.putsession = MagicMock()
            api_common_common.unit_hp_change = MagicMock(return_value=1)
            self.objcard.effect = "unit_1dmg_3times"
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            # api_common_common.unit_hp_changeが3回呼ばれていることを確認
            api_common_common.unit_hp_change.assert_called()
            self.assertEqual(api_common_common.unit_hp_change.call_count, 3)
            # そのうち1回はself.objcard1に対して呼ばれていることを確認
            api_common_common.unit_hp_change.assert_any_call(
                self.sid, self.playview, self.objcard1, 1
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
        # Test case 4-3: Test with dmg_enemy effect 1times of 3
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            playview_end.p1board = [None, None, None, None, None, None]
            play_view_mock.return_value = playview_end
            api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
            card_db.putsession = MagicMock()
            api_common_common.unit_hp_change = MagicMock(return_value=0)
            self.objcard.effect = "unit_1dmg_3times"
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            # api_common_common.unit_hp_changeが1回呼ばれていることを確認
            api_common_common.unit_hp_change.assert_called()
            self.assertEqual(api_common_common.unit_hp_change.call_count, 1)
            # そのうち1回はself.objcard1に対して呼ばれていることを確認
            api_common_common.unit_hp_change.assert_any_call(
                self.sid, self.playview, self.objcard1, 1
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
        self.assertEqual(result, {"error": "target unit has antieffect"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_illegal_card2(self):
        # Test case 6: Test with illegal card2
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        result, status_code = api_spell(
            self.sid, self.playview, self.card1, "dummy_card"
        )
        self.assertEqual(result, {"error": "illegal target"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_illegal_card2_unit(self):
        # Test case 7: Test with illegal card2 unit
        api_common_util.getobjcard = MagicMock(return_value=None)
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"error": "unit don't exists in target"})
        self.assertEqual(status_code, 403)

    def test_api_spell_with_mp_short(self):
        # Test case 8: Test with mp short
        api_common_util.getobjcard = MagicMock(return_value=self.objcard1)
        api_common_util.getobjcard_oppsite = MagicMock(return_value=self.objcard2)
        self.playview.p1mp = 2
        result, status_code = api_spell(self.sid, self.playview, self.card1, self.card2)
        self.assertEqual(result, {"error": "MP short"})
        self.assertEqual(status_code, 403)

    @patch("api_common_tension.api_common_tension_objcard")
    def test_api_spell_with_onspell_effect(self, mock_api_common_tension_objcard):
        # Test case 9: Test with onspell effect
        with patch("api_spell.Play_view") as play_view_mock:
            playview_end = Mock()
            playview_end.p1hp = 10
            playview_end.p2hp = 7
            playview_end.p1.tension = 0
            objcard_onspell = Mock()
            objcard_onspell.effect = "onspell_self:self_tension+1,skillboost+2+2"
            playview_end.p1board = [None, None, None, None, objcard_onspell, None]
            play_view_mock.return_value = playview_end
            card_db.putsession = MagicMock()
            api_common_common.unit_hp_change = MagicMock(return_value=3)
            mock_api_common_tension_objcard.return_value = ("OK", 200)
            result, status_code = api_spell(
                self.sid, self.playview, self.card1, self.card2
            )
            self.assertEqual(result, {"info": "OK"})
            self.assertEqual(status_code, 200)
            mock_api_common_tension_objcard.assert_called_once()


if __name__ == "__main__":
    unittest.main()
