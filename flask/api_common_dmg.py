import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db
import api_common_common
import api_common_util


def api_common_dmg(sid, playview: Play_view, effect, card2, isRun):
    if "dmg" in effect:
        # HP変化系
        # TODO ターゲットフィルタ
        pattern = r"(^.*)_.*"
        matches = re.search(pattern, effect)
        target = matches.group(1)
        pattern = r"[+-]?\d+"
        matches = re.search(pattern, effect)
        value = int(matches.group())

        # 攻撃先確認
        pattern_p1board = r'leftboard_[0-5]$'   # 盤面
        pattern_p1leader = r'leftboard_'  # リーダー
        pattern_p2board = r'rightboard_[0-5]$'   # 盤面
        pattern_p2leader = r'rightboard_10'  # リーダー
        # TODO 自ボード、自リーダーへの攻撃
        if re.match(pattern_p2board, card2):
            # TODO 対象制限の確認

            objcard2 = api_common_util.getobjcard(playview, card2)
            if (objcard2 is None):
                return {"error": "unit don't exists in target card"}, 403
            # ALL OK DB更新
            # 対象ユニットHP減算
            if isRun:
                card_db.appendlog(playview.playdata.card_table,
                                  "effect->" + objcard2.name)
                api_common_common.unit_hp_change(
                    sid, playview, objcard2, value)
        elif re.match(pattern_p2leader, card2):
            # リーダーHP減算
            if isRun:
                card_db.appendlog(playview.playdata.card_table,
                                  "effect->" + playview.p2name)
                api_common_common.p2leader_hp_change(playview, value)
    else:
        return {"error": "unit don't exists in target card"}, 403

    return "OK", 200
