import unittest
from unittest.mock import Mock, patch

import card_db
from api_common_common import leader_hp_change, unit_hp_change, unit_hp_change_multi


class TestUnitHPChangeMulti(unittest.TestCase):
    def test_unit_hp_change_multi(self):
        # テスト用のダミーデータと引数を設定
        sid = "test_sid"
        playview = Mock()
        playview.playdata.card_table = "test_card_table"
        objcard1 = Mock()
        objcard1.hp_org = 5  # 仮のhp_org値
        objcard1.dhp = 0  # 仮のdhp値
        objcard1.status = [""]
        objcard1.name = "test_name1"
        objcard2 = Mock()
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = 0  # 仮のdhp値
        objcard2.status = [""]
        objcard2.name = "test_name2"
        objcards = [objcard1, objcard2]
        values = [3, 2]  # 減算する値

        # objcard1, objcard2のrefreshメソッドをモック化
        objcard1.refresh = Mock()
        objcard2.refresh = Mock()
        # card_db.appendlog関数をモック化
        card_db.appendlog = Mock()

        # card_db.putsession関数をモック化
        # api_common_util.get_self_or_enemyの戻り値をモック化
        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change_multi関数を呼び出す
            unit_hp_change_multi(sid, playview, objcards, values)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard1.cuid,
                "dhp",
                -3,  # 期待されるdhp値
            )
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -2,  # 期待されるdhp値
            )

        # objcard1, objcard2のhp_org + dhpが0以下の場合のテスト
        objcard1.hp_org = 5  # 仮のhp_org値
        objcard1.dhp = -3  # 仮のdhp値
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = -2  # 仮のdhp値

        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch("api_common_dead.ondead") as mock_ondead:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change_multi関数を呼び出す
            unit_hp_change_multi(sid, playview, objcards, values)

            # card_db.putsessionが3回呼ばれたかチェック
            self.assertEqual(mock_putsession.call_count, 3)

            # 1回目の呼び出しの検証
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard1.cuid,
                "dhp",
                -6,  # 期待されるdhp値
            )

            # 2回目の呼び出しの検証
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard1.cuid,
                "loc",
                "player_self_cemetery",
            )

            # 3回目の呼び出しの検証
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -4,  # 期待されるdhp値
            )

            # 他の関数が正しく呼び出されたかも検証できるようにモック化
            # api_common_util.get_self_or_enemy, api_common_dead.ondead など
            # api_common_dead.ondeadが呼ばれたかチェック
            mock_ondead.assert_called_once_with(sid, playview, objcard1)

        # objcard1, objcard2のstatusにmetalbodyが含まれる場合のテスト
        objcard1.hp_org = 5
        objcard1.dhp = 0
        objcard1.status = ["metalbody"]
        objcard2.hp_org = 5
        objcard2.dhp = 0
        objcard2.status = ["metalbody"]

        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch("api_common_dead.ondead") as mock_ondead:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change_multi関数を呼び出す
            unit_hp_change_multi(sid, playview, objcards, values)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard1.cuid,
                "dhp",
                -1,  # 期待されるdhp値
            )
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -1,  # 期待されるdhp値
            )


class TestUnitHPChange(unittest.TestCase):
    def test_unit_hp_change(self):
        # テスト用のダミーデータと引数を設定
        sid = "test_sid"
        playview = Mock()
        playview.playdata.card_table = "test_card_table"
        objcard2 = Mock()
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = 0  # 仮のdhp値
        objcard2.status = [""]
        objcard2.name = "test_name"
        value = 3  # 減算する値

        # objcard2のrefreshメソッドをモック化
        objcard2.refresh = Mock()
        # card_db.appendlog関数をモック化
        card_db.appendlog = Mock()

        # card_db.putsession関数をモック化
        # api_common_util.get_self_or_enemyの戻り値をモック化
        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)

            # objcard2のrefreshメソッドが呼ばれたことを確認
            objcard2.refresh.assert_called_once_with(playview.playdata.card_table)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -3,  # 期待されるdhp値
            )

        # objcard2のhp_org + dhpが0以下の場合のテスト
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = -3  # 仮のdhp値

        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch("api_common_dead.ondead") as mock_ondead:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)

            # card_db.putsessionが2回呼ばれたかチェック
            self.assertEqual(mock_putsession.call_count, 2)

            # 1回目の呼び出しの検証
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -6,  # 期待されるdhp値
            )

            # 2回目の呼び出しの検証
            mock_putsession.assert_any_call(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "loc",
                "player_self_cemetery",
            )

            # 他の関数が正しく呼び出されたかも検証できるようにモック化
            # api_common_util.get_self_or_enemy, api_common_dead.ondead など
            # api_common_dead.ondeadが呼ばれたかチェック
            mock_ondead.assert_called_once_with(sid, playview, objcard2)

        # objcard.statusにmetalbodyが含まれる場合のテスト
        objcard2.hp_org = 5
        objcard2.dhp = 0
        objcard2.status = ["metalbody"]

        with patch("card_db.putsession") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch("api_common_dead.ondead") as mock_ondead:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                playview.playdata.card_table,
                "cuid",
                objcard2.cuid,
                "dhp",
                -1,  # 期待されるdhp値
            )


class TestLeaderHPChange(unittest.TestCase):
    def test_leader_hp_change(self):
        # テスト用のダミーデータと引数を設定
        player = Mock()
        player.player_tid = 1
        player.hp = 100  # 仮のHP値
        value = 10  # 減算する値

        # cards_db.putsession関数をモック化
        with patch("card_db.putsession") as mock_putsession:
            # leader_hp_change関数を呼び出す
            leader_hp_change(player, value)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                "playerstats", "player_tid", 1, "hp", 90  # 期待されるHP値
            )


if __name__ == "__main__":
    unittest.main()
