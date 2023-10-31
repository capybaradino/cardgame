import unittest
from unittest.mock import MagicMock, Mock, patch

import api_common_util
import card_db
from api_common_status import api_common_active


class TestAPICommonActive(unittest.TestCase):
    def test_api_common_active(self):
        # テスト用のダミー引数を設定
        sid = 1
        playview = Mock()
        effect = "active"
        card2 = "dummy_card"
        isRun = True

        # 子関数のMock化
        api_common_util.getobjcard = MagicMock()
        api_common_util.get_self_or_enemy = MagicMock(
            return_value=[None, None, None, None]
        )
        card_db.putsession = MagicMock()

        # 事前チェックは不要の場合のテスト
        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_active(sid, playview, effect, card2, False)
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)
            # card_db.putsessionが呼ばれていない事をチェック
            mock_putsession.assert_not_called()

        # 事前チェックが必要な場合のテスト

        # 自分自身をactive化するパターン
        effect = "onplay:self_active"
        with patch("card_db.putsession") as mock_putsession:
            result, status_code = api_common_active(sid, playview, effect, card2, isRun)
            self.assertEqual(result, "OK")
            self.assertEqual(status_code, 200)

            # card_db.putsessionが呼ばれたかチェック
            mock_putsession.assert_called_once()

        # "active"以外のeffectの場合のテスト
        effect = "other_effect"
        with self.assertRaises(Exception):
            api_common_active(sid, playview, effect, card2, isRun)


if __name__ == "__main__":
    unittest.main()
