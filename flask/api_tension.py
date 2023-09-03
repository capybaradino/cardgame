import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_tension(sid, playview: Play_view, card1, card2):
    # テンション・テンションスキル
    # テンション値確認
    tension = playview.p1tension
    if (tension < 3):
        # テンションアップ
        # MP減算
        remainingmp = playview.p1mp - 1
        if (remainingmp < 0):
            return {"error": "MP short"}
        card_db.putsession("playerstats",
                           "name", playview.p1name,
                           "mp", remainingmp)
        tension = tension + 1
        card_db.putsession("playerstats",
                           "name", playview.p1name,
                           "tension", tension)
    else:
        # テンションスキル発動
        # TODO wizのみ対応

        # 攻撃先確認
        pattern_p1board = r'rightboard_[0-5]$'   # 盤面
        pattern_p1leader = r'rightboard_10'  # リーダー
        pattern_p2board = r'rightboard_[0-5]$'   # 盤面
        pattern_p2leader = r'rightboard_10'  # リーダー
        # TODO 自ボード、自リーダーへの攻撃
        value = 3
        if re.match(pattern_p2board, card2):
            # ボードの確認
            pattern = r'[0-5]'
            number = int(re.findall(pattern, card2)[0])
            boards = playview.p2board
            objcard2: Card_info
            objcard2 = boards[number]
            if (objcard2 is None):
                return {"error": "unit don't exists in card2"}, 403
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
            # テンション初期化
            tension = 0
            card_db.putsession("playerstats",
                               "name", playview.p1name,
                               "tension", tension)
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
            # テンション初期化
            tension = 0
            card_db.putsession("playerstats",
                               "name", playview.p1name,
                               "tension", tension)
            if (newhp <= 0):
                playview.playdata.gamewin(sid)
        else:
            return {"error": "illegal card2"}, 403

    return {"info": "OK"}
