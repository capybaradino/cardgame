import unittest
from unittest.mock import Mock, patch

import api_common_util
import card_db
from card_turnend import card_turnend


class TestCardTurnend(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.state = "p1turn"
        self.nickname = "test_player_1"
        self.playdata = Mock()
        self.playdata.state = self.state
        self.playdata.gsid = 1
        self.mock_playdata.return_value = self.playdata
        self.playview = Mock()
        self.playview.playdata = self.playdata
        self.p1objcard = Mock()
        self.p1objcard.dattack = 0
        self.p2objcard = Mock()
        self.p2objcard.dattack = 0
        self.playview.p1board = [self.p1objcard for _ in range(4)]
        self.playview.p2board = [self.p2objcard for _ in range(4)]
        self.playview.p1name = self.nickname
        self.playview.p2name = "test_player_2"
        self.playview.p1 = Mock()
        self.playview.p2 = Mock()
        self.playview.p1.draw_card = Mock()
        self.playview.p2.draw_card = Mock()
        self.mock_playview.return_value = self.playview
        self.mock_get_self_or_enemy.return_value = (
            Mock(),
            Mock(),
            self.playview.p2,
            Mock(),
        )

    mock_playdata = Mock()
    mock_playview = Mock()
    mock_putsession = Mock()
    mock_putgamesession = Mock()
    mock_get_self_or_enemy = Mock()
    mock_cardcommon_judge = Mock()

    def tearDown(self):
        self.mock_playdata.reset_mock()
        self.mock_playview.reset_mock()
        self.mock_putsession.reset_mock()
        self.mock_putgamesession.reset_mock()
        self.mock_get_self_or_enemy.reset_mock()

    # p1ターン終了時のテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    def test_card_turnend_with_p1turn(self):
        self.state = "p1turn"
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "onturnend_self_each:1draw_any", ""]
            for _ in range(1)
        ]
        self.mock_get_self_or_enemy.return_value = (
            Mock(),
            Mock(),
            self.playview.p1,
            Mock(),
        )
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(card_db.putgamesession.call_args[0][1], "state")
        self.assertEqual(card_db.putgamesession.call_args[0][2], "p2turn")
        # Mockが2回呼ばれていることを確認
        self.assertEqual(self.playview.p1.draw_card.call_count, 2)

    # p1ターン終了時のテスト(条件が自ユニットだけの場合)
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    @patch("card_common.judge", mock_cardcommon_judge)
    def test_card_turnend_with_p1turn(self):
        self.state = "p1turn"
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "onturnend_self:1draw_any", ""]
            for _ in range(1)
        ]
        self.mock_get_self_or_enemy.return_value = (
            Mock(),
            Mock(),
            self.playview.p1,
            Mock(),
        )
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(card_db.putgamesession.call_args[0][1], "state")
        self.assertEqual(card_db.putgamesession.call_args[0][2], "p2turn")
        # Mockが1回呼ばれていることを確認
        self.assertEqual(self.playview.p1.draw_card.call_count, 1)

    # p2ターン終了時のテスト(ユニット数、片方４体の場合)
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    @patch("card_common.judge", mock_cardcommon_judge)
    def test_card_turnend_with_p2turn(self):
        self.state = "p2turn"
        self.playdata.state = self.state
        self.mock_playdata.return_value = self.playdata
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "onturnend_self_each:1draw_any", ""]
            for _ in range(4)
        ]
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(self.mock_putgamesession.call_args[0][1], "state")
        self.assertEqual(self.mock_putgamesession.call_args[0][2], "p1turn")
        # Mockが2回呼ばれていることを確認
        self.assertEqual(self.playview.p2.draw_card.call_count, 8)

    # 無効なstateのテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    def test_card_turnend_with_invalid_state(self):
        self.playdata.state = "invalid_state"
        with self.assertRaises(Exception):
            card_turnend(self.sid, self.state, self.nickname)

    # ボードテーブルにエフェクトを持つカードがいない場合のテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    def test_card_turnend_with_no_effect(self):
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "", ""] for _ in range(4)
        ]
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(card_db.putgamesession.call_args[0][1], "state")
        self.assertEqual(card_db.putgamesession.call_args[0][2], "p2turn")
        self.playview.p1.draw_card.assert_not_called()
        self.playview.p2.draw_card.assert_not_called()

    # 無効なキーワードを持つカードがいる場合のテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    def test_card_turnend_with_unknown_keyword(self):
        self.mock_playdata.return_value = self.playdata
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "unknown_keyword:1draw", ""]
            for _ in range(4)
        ]
        card_turnend(self.sid, self.state, self.nickname)
        self.playview.p1.draw_card.assert_not_called()
        self.playview.p2.draw_card.assert_not_called()

    # エフェクトを複数持つカードがいる場合のテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    @patch("card_common.judge", mock_cardcommon_judge)
    def test_card_turnend_with_multiple_effects(self):
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [
                0,
                0,
                "test_cuid",
                0,
                0,
                0,
                "",
                "onturnend_self_each:1draw_any,onturnend_self_each:1draw_any",
                "",
            ]
            for _ in range(1)
        ]
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(self.playview.p2.draw_card.call_count, 4)
        self.playview.p1.draw_card.assert_not_called()

    # attack値変更のテスト
    @patch("card_turnend.Playdata", mock_playdata)
    @patch("card_turnend.Play_view", mock_playview)
    @patch("card_db.putcardtable", mock_putsession)
    @patch("card_db.putgamesession", mock_putgamesession)
    @patch("api_common_util.get_self_or_enemy", mock_get_self_or_enemy)
    def test_card_turnend_with_attack_effect(self):
        self.mock_playdata.return_value = self.playdata
        self.mock_playview.return_value = self.playview
        card_db.getrecords_fromsession = Mock()
        card_db.getrecords_fromsession.return_value = [
            [0, 0, "test_cuid", 0, 0, 0, "", "", "self_attack-2"] for _ in range(4)
        ]
        card_turnend(self.sid, self.state, self.nickname)
        self.assertEqual(
            card_db.putcardtable.call_args_list[0][0][4],
            self.playview.p1board[0].dattack - 2,
        )
        self.playview.p1.draw_card.assert_not_called()
        self.playview.p2.draw_card.assert_not_called()


# メイン関数の呼び出し
if __name__ == "__main__":
    unittest.main()
