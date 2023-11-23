import unittest
from unittest.mock import Mock, patch

import card_db
from class_playview import Play_view


class TestPlayView(unittest.TestCase):
    def setUp(self):
        self.sid = 1
        self.nickname = "test_player_1"
        self.playdata = Mock()
        self.playdata.player1 = Mock()
        self.playdata.player2 = Mock()
        self.playdata.state = "p1turn"
        self.playdata.card_table = "test_card_table"
        self.playdata.player1.get_hand = Mock(return_value=[])
        self.playdata.player2.get_hand = Mock(return_value=[])
        self.playdata.player1.name = "test_player_1"
        self.playdata.player2.name = "test_player_2"
        self.playdata.p2board = [None, None, None, None, None, None]
        self.mock_playdata.return_value = self.playdata
        self.mock_getnickname_fromsid.return_value = self.nickname
        self.mock_getcards_fromdeck.return_value = []

    mock_playdata = Mock()
    mock_getnickname_fromsid = Mock()
    mock_getcards_fromdeck = Mock()

    # 初期化テスト
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_init(self):
        play_view = Play_view(self.sid)

        self.assertEqual(play_view.sid, self.sid)
        self.assertEqual(play_view.playdata, self.playdata)
        self.assertEqual(play_view.turnstate, self.playdata.state)
        self.assertEqual(play_view.p1, self.playdata.player1)
        self.assertEqual(play_view.p2, self.playdata.player2)
        self.assertEqual(play_view.p1name, self.playdata.player1.name)
        self.assertEqual(play_view.p2name, self.playdata.player2.name)
        self.assertEqual(play_view.p2hp, self.playdata.player2.hp)
        self.assertEqual(play_view.p2job, self.playdata.player2.job)
        self.assertEqual(play_view.p2decknum, self.playdata.player2.get_decknum())
        self.assertEqual(play_view.p2mp, self.playdata.player2.mp)
        self.assertEqual(play_view.p2maxmp, self.playdata.player2.maxmp)
        self.assertEqual(play_view.p2tension, self.playdata.player2.tension)
        self.assertEqual(play_view.p2handnum, 0)
        self.assertEqual(len(play_view.p2hand), 10)
        self.assertEqual(play_view.p1board, [None, None, None, None, None, None])
        self.assertEqual(play_view.p2board, [None, None, None, None, None, None])
        self.assertEqual(play_view.p1hp, self.playdata.player1.hp)
        self.assertEqual(play_view.p1job, self.playdata.player1.job)
        self.assertEqual(play_view.p1decknum, self.playdata.player1.get_decknum())
        self.assertEqual(play_view.p1mp, self.playdata.player1.mp)
        self.assertEqual(play_view.p1maxmp, self.playdata.player1.maxmp)
        self.assertEqual(play_view.p1tension, self.playdata.player1.tension)
        self.assertEqual(
            play_view.p1hand,
            [None, None, None, None, None, None, None, None, None, None],
        )
        self.assertEqual(len(play_view.p1hand), 10)

    # ブロック可能判定テスト
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_isblockable_with_board_not_none(self):
        play_view = Play_view(self.sid)
        board = Mock()
        board.status = ""

        result = play_view.isblockable(board)

        self.assertTrue(result)

    # ユニットがいない場合はブロック不可判定
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_isblockable_with_board_none(self):
        play_view = Play_view(self.sid)
        board = None

        result = play_view.isblockable(board)

        self.assertFalse(result)

    # 前衛にいる場合(ブロック無し)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_isblocked_with_number_less_than_3(self):
        play_view = Play_view(self.sid)
        number = 2

        result = play_view.isblocked(number)

        self.assertFalse(result)

    # 後衛にいて、前のユニットがブロック可能な場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_isblocked_with_blockable_front_unit(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=True)
        play_view._hasfortress = Mock(return_value=False)
        number = 3

        result = play_view.isblocked(number)

        self.assertTrue(result)

    # 後衛だが、前のユニットがブロック不可能な場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_isblocked_with_unblockable_front_unit(self):
        number = 3
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=False)

        result = play_view.isblocked(number)

        self.assertFalse(result)

    def mock_cardinfo_update(self):
        self.status = "some_effect"

    # 前衛だが、仁王立ちユニットがいる場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    @patch("class_playdata.Card_info.update", new=mock_cardinfo_update)
    def test_isblocked_with_no_front_unit_and_no_fortress(self):
        number = 1
        self.mock_getcards_fromdeck.return_value = [
            [0, 0, 0, number, 0, 0, "card_table"]
        ]
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=True)

        result = play_view.isblocked(number)

        self.assertTrue(result)

    # 後衛で、仁王立ちユニットがいる場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    @patch("class_playdata.Card_info.update", new=mock_cardinfo_update)
    def test_isblocked_with_no_front_unit_but_has_fortress(self):
        number = 4
        self.mock_getcards_fromdeck.return_value = [
            [0, 0, 0, number, 0, 0, "card_table"]
        ]
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=True)

        result = play_view.isblocked(number)

        self.assertTrue(result)

    def mock_cardinfo_update_fortress(self):
        self.status = "fortress"

    # 後衛で、仁王立ちユニットがいる場合(自分も仁王立ち持ちだが後衛なのでブロックされる)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    @patch("class_playdata.Card_info.update", new=mock_cardinfo_update_fortress)
    def test_isblocked_with_no_front_unit_but_has_fortress(self):
        number = 4
        self.mock_getcards_fromdeck.return_value = [
            [0, 0, 0, number, 0, 0, "card_table"]
        ]
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=True)

        result = play_view.isblocked(number)

        self.assertTrue(result)

    # 前衛で、仁王立ちユニットがいる場合(自分も仁王立ち持ちなのでブロック対象外)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    @patch("class_playdata.Card_info.update", new=mock_cardinfo_update_fortress)
    def test_isblocked_with_no_front_unit_but_has_fortress(self):
        number = 0
        self.mock_getcards_fromdeck.return_value = [
            [0, 0, 0, number, 0, 0, "card_table"]
        ]
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=True)

        result = play_view.isblocked(number)

        self.assertFalse(result)

    # 仁王立ち有無テスト(ユニット無し)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test__hasfortress_with_no_fortress(self):
        play_view = Play_view(self.sid)
        play_view.p2board = [None, None, None, None, None, None]

        result = play_view._hasfortress()

        self.assertFalse(result)

    # 仁王立ち有無テスト(ユニット有り)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test__hasfortress_with_fortress_present(self):
        play_view = Play_view(self.sid)
        play_view.p2board = [Mock(status=["fortress"]), None, None, None, None, None]

        result = play_view._hasfortress()

        self.assertTrue(result)

    # ウォールが無く仁王立ちもいない場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_iswall_with_no_blockable_units(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=False)

        result = play_view.iswall()

        self.assertFalse(result)

    # ウォールあり、仁王立ち無し
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_iswall_with_blockable_units_in_all_rows(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=True)
        play_view._hasfortress = Mock(return_value=False)

        result = play_view.iswall()

        self.assertTrue(result)

    # 2体ブロック可能(=ウォール無し)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_iswall_with_blockable_units_in_some_rows(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(
            side_effect=[True, False, True, False, False, False]
        )
        play_view._hasfortress = Mock(return_value=False)

        result = play_view.iswall()

        self.assertFalse(result)

    # 3体ブロック可能(=ウォールあり)
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_iswall_with_blockable_units_in_some_rows(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(
            side_effect=[True, False, True, False, False, True]
        )
        play_view._hasfortress = Mock(return_value=False)

        result = play_view.iswall()

        self.assertTrue(result)

    # ウォールは無いが仁王立ちがいる場合
    @patch("class_playview.Playdata", mock_playdata)
    @patch("card_db.getnickname_fromsid", mock_getnickname_fromsid)
    @patch("card_db.getcards_fromdeck", mock_getcards_fromdeck)
    def test_iswall_with_no_blockable_units_but_has_fortress(self):
        play_view = Play_view(self.sid)
        play_view.isblockable = Mock(return_value=False)
        play_view._hasfortress = Mock(return_value=True)

        result = play_view.iswall()

        self.assertTrue(result)


# メイン関数の呼び出し
if __name__ == "__main__":
    unittest.main()
