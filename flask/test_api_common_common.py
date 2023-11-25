import unittest
from unittest.mock import Mock, patch

import api_common_common
import api_common_tension
import card_db
from api_common_common import (
    api_common_dmg,
    api_common_dmg_leader,
    leader_hp_change,
    unit_hp_change,
    unit_hp_change_multi,
)


class TestApiCommonDmg(unittest.TestCase):
    @patch("re.search")
    @patch("api_common_common.unit_hp_change")
    def test_api_common_dmg(self, mock_unit_hp_change, mock_search):
        # Mockオブジェクトの設定
        mock_search.return_value.group.side_effect = ["target", "10"]
        mock_unit_hp_change.return_value = 10
        # card_db.appendlog関数をモック化
        card_db.appendlog = Mock()

        # テスト対象の関数を呼び出す
        sid = "test_sid"
        playview = Mock()  # Play_viewのMockオブジェクト
        effect = "test_effect"
        objcard2 = Mock()  # Card_infoのMockオブジェクト
        objcard2.name = "test_name"
        result = api_common_dmg(sid, playview, effect, objcard2, True)

        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))

        # Mockオブジェクトが期待通りに呼び出されたことを確認
        mock_search.assert_any_call(r"(^.*)_.*", effect)
        mock_search.assert_any_call(r"[+-]?\d+", effect)
        mock_unit_hp_change.assert_called_once_with(sid, playview, objcard2, 10)


class TestApiCommonDmgLeader(unittest.TestCase):
    @patch("re.search")
    @patch("api_common_common.leader_hp_change")
    def test_api_common_dmg_leader(self, mock_leader_hp_change, mock_search):
        # Mockオブジェクトの設定
        mock_search.return_value.group.side_effect = ["target", "10"]
        mock_leader_hp_change.return_value = None

        # テスト対象の関数を呼び出す
        sid = "test_sid"
        playview = Mock()  # Play_viewのMockオブジェクト
        playview.p2name = "test_p2name"
        playview.p2 = "test_p2"
        effect = "test_effect"
        result = api_common_dmg_leader(sid, playview, effect, True)

        # 戻り値の確認
        self.assertEqual(result, ("OK", 200))

        # Mockオブジェクトが期待通りに呼び出されたことを確認
        mock_search.assert_any_call(r"(^.*)_.*", effect)
        mock_search.assert_any_call(r"[+-]?\d+", effect)
        mock_leader_hp_change.assert_called_once_with(playview.p2, 10)


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
        objcard1.effect = "test_effect"
        objcard2 = Mock()
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = 0  # 仮のdhp値
        objcard2.status = [""]
        objcard2.name = "test_name2"
        objcard2.effect = "test_effect"
        objcards = [objcard1, objcard2]
        values = [3, 2]  # 減算する値

        # objcard1, objcard2のrefreshメソッドをモック化
        objcard1.refresh = Mock()
        objcard2.refresh = Mock()
        # card_db.appendlog関数をモック化
        card_db.appendlog = Mock()

        # card_db.putsession関数をモック化
        # api_common_util.get_self_or_enemyの戻り値をモック化
        with patch("card_db.putcardtable") as mock_putsession, patch(
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

        with patch("card_db.putcardtable") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch(
            "api_common_common._ondead_effect"
        ) as mock_ondead:
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

        with patch("card_db.putcardtable") as mock_putsession, patch(
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
    mock_cardcommon_judge = Mock()

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
        with patch("card_db.putcardtable") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)

            # objcard2のrefreshメソッドが呼ばれたことを確認
            objcard2.refresh.assert_called_once_with()

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

        with patch("card_db.putcardtable") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch(
            "api_common_common._ondead_effect"
        ) as mock_ondead:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            mock_get_self_or_enemy.return_value = [Mock(), Mock(), player_self, Mock()]

            # ondeadの対象外にする
            objcard2.effect = "test_effect"

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

        with patch("card_db.putcardtable") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy:
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

    @patch("card_common.judge", mock_cardcommon_judge)
    def test_unit_hp_change_with_ondead_effect(self):
        # effectにondeadが含まれる場合のテスト
        # テスト用のダミーデータと引数を設定
        sid = "test_sid"
        playview = Mock()
        playview.playdata.card_table = "test_card_table"
        objcard2 = Mock()
        objcard2.hp_org = 5  # 仮のhp_org値
        objcard2.dhp = -2  # 仮のdhp値
        objcard2.status = [""]
        objcard2.name = "test_name"
        value = 3  # 減算する値

        # objcard2のrefreshメソッドをモック化
        objcard2.refresh = Mock()
        # card_db.appendlog関数をモック化
        card_db.appendlog = Mock()

        # card_db.putsession関数をモック化
        # api_common_util.get_self_or_enemyの戻り値をモック化
        with patch("card_db.putcardtable") as mock_putsession, patch(
            "api_common_util.get_self_or_enemy"
        ) as mock_get_self_or_enemy, patch(
            "api_common_tension.api_common_tension_objcard"
        ) as mock_tension_objcard:
            # api_common_util.get_self_or_enemyの戻り値をモック化
            player_self = Mock()
            player_self.name = "player_self"
            card = Mock()
            card.hp_org = 5
            card.dhp = 0
            card.name = "test_name"
            player_enemy = Mock()
            player_enemy.name = "test_name"
            mock_get_self_or_enemy.return_value = [
                Mock(),
                [card],
                player_self,
                player_enemy,
            ]

            # tensionのテスト
            objcard2.effect = "ondead:self_tension+1"
            mock_tension_objcard.return_value = ("OK", 200)
            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)
            # Mockオブジェクトが期待通りに呼び出されたことを確認
            mock_tension_objcard.assert_called_once()

            with patch("random.randrange") as mock_randrange:
                # dmgのテスト(対象がユニット)
                objcard2.effect = "ondead:enemy_1dmg_random"
                api_common_common.unit_hp_change = Mock(return_value=("OK", 200))
                mock_randrange.return_value = 0
                # unit_hp_change関数を呼び出す
                unit_hp_change(sid, playview, objcard2, value)
                # Mockオブジェクトが期待通りに呼び出されたことを確認
                api_common_common.unit_hp_change.assert_called_once()

                # dmgのテスト(対象がリーダー)
                objcard2.effect = "ondead:enemy_1dmg_random"
                api_common_common.leader_hp_change = Mock(return_value=("OK", 200))
                mock_randrange.return_value = 1
                # unit_hp_change関数を呼び出す
                unit_hp_change(sid, playview, objcard2, value)
                # Mockオブジェクトが期待通りに呼び出されたことを確認
                api_common_common.leader_hp_change.assert_called_once()

            # drawのテスト(対象が自リーダー)
            objcard2.effect = "ondead:self_1draw_spell"
            player_self.draw_card_spell = Mock()
            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)
            # Mockオブジェクトが期待通りに呼び出されたことを確認
            player_self.draw_card_spell.assert_called_once()

            # drawのテスト(対象が敵リーダー)
            objcard2.effect = "ondead:enemy_1draw_any"
            player_enemy.draw_card = Mock()
            # unit_hp_change関数を呼び出す
            unit_hp_change(sid, playview, objcard2, value)
            # Mockオブジェクトが期待通りに呼び出されたことを確認
            player_enemy.draw_card.assert_called_once()


class TestLeaderHPChange(unittest.TestCase):
    def test_leader_hp_change(self):
        # テスト用のダミーデータと引数を設定
        player = Mock()
        player.player_tid = 1
        player.hp = 100  # 仮のHP値
        value = 10  # 減算する値

        # cards_db.putsession関数をモック化
        with patch("card_db.putplayerstats") as mock_putsession:
            # leader_hp_change関数を呼び出す
            leader_hp_change(player, value)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                "player_tid", 1, "hp", 90  # 期待されるHP値
            )


if __name__ == "__main__":
    unittest.main()
