import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_spell(sid, playview: Play_view, card1, card2):
    # 特技使用
    pattern = r'[0-9]'
    number = int(re.findall(pattern, card1)[0])
    hands = playview.p1hand
    objcard1: Card_info
    objcard1 = hands[number]
    if (objcard1 is None):
        return {"error": "illegal card1 number"}, 403

    # MP減算
    remainingmp = playview.p1mp - objcard1.cost
    if (remainingmp < 0):
        return {"error": "MP short"}
    card_db.putsession("playerstats",
                       "name", playview.p1name,
                       "mp", remainingmp)

    # TODO 多種特技の内容対応
    effect_array = objcard1.effect.split(",")
    # 特技の対象確認
    for effect in effect_array:
        if "dmg" in effect:
            # HP変化系
            pattern = r"(^.*)_.*"
            matches = re.search(pattern, effect)
            target = matches.group(1)
            pattern = r"\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())

            # 攻撃先確認
            pattern_p1board = r'rightboard_[0-5]$'   # 盤面
            pattern_p1leader = r'rightboard_10'  # リーダー
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
                # カード状態変更
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard1.cuid,
                                   "loc", playview.p1name + "_cemetery")
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
                # カード状態変更
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard1.cuid,
                                   "loc", playview.p1name + "_cemetery")
                if (newhp <= 0):
                    playview.playdata.gamewin(sid)
            else:
                return {"error": "illegal card2"}, 403

    return {"info": "OK"}
