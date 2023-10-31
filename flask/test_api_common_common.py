import unittest
from unittest.mock import Mock, patch

from api_common_common import leader_hp_change, p2leader_hp_change


class TestLeaderHPChange(unittest.TestCase):
    def test_leader_hp_change(self):
        # テスト用のダミーデータと引数を設定
        playview = Mock()
        player = Mock()
        player.player_tid = 1
        player.hp = 100  # 仮のHP値
        value = 10  # 減算する値

        # cards_db.putsession関数をモック化
        with patch("card_db.putsession") as mock_putsession:
            # leader_hp_change関数を呼び出す
            leader_hp_change(playview, player, value)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                "playerstats", "player_tid", 1, "hp", 90  # 期待されるHP値
            )


class TestP2LeaderHPChange(unittest.TestCase):
    def test_p2leader_hp_change(self):
        # テスト用のダミーデータと引数を設定
        playview = Mock()
        playview.p2hp = 100  # 仮のp2のHP値
        value = 10  # 減算する値

        # プレイヤー名を設定
        playview.playdata.player1.name = "player1"
        playview.p1name = "player1"

        # cards_db.putsession関数をモック化
        with patch("card_db.putsession") as mock_putsession:
            # p2leader_hp_change関数を呼び出す
            p2leader_hp_change(playview, value)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once_with(
                "playerstats",
                "player_tid",
                playview.playdata.p2_player_tid,
                "hp",
                90,  # 期待されるp2のHP値
            )

        # プレイヤー名を入れ替えて再度テスト
        playview.playdata.player1.name = "player2"
        playview.p1name = "player1"  # 仮に異なる名前を設定

        with patch("card_db.putsession") as mock_putsession:
            p2leader_hp_change(playview, value)

            mock_putsession.assert_called_once_with(
                "playerstats",
                "player_tid",
                playview.playdata.p1_player_tid,
                "hp",
                90,  # 期待されるp1のHP値
            )


if __name__ == "__main__":
    unittest.main()
