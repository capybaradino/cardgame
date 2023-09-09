import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_common_dmg(sid, playview: Play_view, effect, card2):
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

            # ボードの確認
            pattern = r'[0-5]'
            number = int(re.findall(pattern, card2)[0])
            boards = playview.p2board
            objcard2: Card_info
            objcard2 = boards[number]
            if (objcard2 is None):
                return {"error": "unit don't exists in target card"}, 403
            # ALL OK DB更新
            # 対象ユニットHP減算
            dhp = objcard2.dhp - value
            card_db.putsession(playview.playdata.card_table,
                               "cuid", objcard2.cuid,
                               "dhp", dhp)
            if (objcard2.hp_org + dhp <= 0):
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard2.cuid,
                                   "loc", playview.p2name + "_cemetery")
        elif re.match(pattern_p2leader, card2):
            # リーダーHP減算
            newhp = playview.p2hp - value
            if (playview.playdata.player1.name == playview.p1name):
                card_db.putsession("playerstats",
                                   "player_tid", playview.playdata.p2_player_tid,
                                   "hp", newhp)
            else:
                card_db.putsession("playerstats",
                                   "player_tid", playview.playdata.p1_player_tid,
                                   "hp", newhp)
    else:
        return {"error": "unit don't exists in target card"}, 403

    return "OK", 200
