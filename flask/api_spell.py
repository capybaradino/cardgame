import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db
import api_common_common
import api_common_util


def api_spell(sid, playview: Play_view, card1, card2):
    # 特技使用
    pattern = r'[0-9]'
    number = int(re.findall(pattern, card1)[0])
    hands = playview.p1hand
    objcard1: Card_info
    objcard1 = hands[number]
    if (objcard1 is None):
        return {"error": "illegal card1 number"}, 403

    # TODO 多種特技の内容対応
    effect_array = objcard1.effect.split(",")
    # 特技の対象確認
    for effect in effect_array:
        if "self_1drow" in effect:
            playview.p1.draw_card()
            card_db.appendlog(playview.playdata.card_table,
                              "["+playview.p1name+"]spell:" + objcard1.name)

        if "switch" in effect:
            # 対象確認
            pattern_p1board = r'leftboard_[0-5]$'   # 盤面
            pattern_p2board = r'rightboard_[0-5]$'   # 盤面
            if re.match(pattern_p2board, card2) or re.match(pattern_p1board, card2):
                # TODO 対象制限の確認
                objcard2 = api_common_util.getobjcard(playview, card2)
                if (objcard2 is None):
                    return {"error": "unit don't exists in card2"}, 403
                # ALL OK DB更新
                card_db.appendlog(playview.playdata.card_table,
                                  "["+playview.p1name+"]spell:" + objcard1.name)
                card_db.appendlog(playview.playdata.card_table,
                                  "target->" + objcard2.name)
                # 対象ユニット場所入れ替え
                objcard3, loc1, loc2 = api_common_util.getobjcard_oppsite(
                    playview, card2)
                card_db.putdeck_locnum(playview.playdata.card_table,
                                       objcard2.cuid, loc2)
                if objcard3 is not None:
                    card_db.putdeck_locnum(playview.playdata.card_table,
                                           objcard3.cuid, loc1)

            else:
                return {"error": "illegal card2"}, 403

        if "dmg" in effect:
            # HP変化系
            pattern = r"(^.*)_.*"
            matches = re.search(pattern, effect)
            target = matches.group(1)
            pattern = r"\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())

            # 攻撃先確認
            pattern_p1board = r'leftboard_[0-5]$'   # 盤面
            pattern_p1leader = r'leftboard_10'  # リーダー
            pattern_p2board = r'rightboard_[0-5]$'   # 盤面
            pattern_p2leader = r'rightboard_10'  # リーダー
            if re.match(pattern_p2board, card2) or re.match(pattern_p1board, card2):
                # TODO 対象制限の確認
                objcard2 = api_common_util.getobjcard(playview, card2)
                if (objcard2 is None):
                    return {"error": "unit don't exists in card2"}, 403

                # 特技無効チェック
                if (card2 is not None):
                    if ("antieffect" in objcard2.status):
                        return {"error": "card2 has antieffect"}, 403

                # ALL OK DB更新
                card_db.appendlog(playview.playdata.card_table,
                                  "["+playview.p1name+"]spell:" + objcard1.name)
                card_db.appendlog(playview.playdata.card_table,
                                  "target->" + objcard2.name)
                # MP減算
                remainingmp = playview.p1mp - objcard1.cost
                if (remainingmp < 0):
                    return {"error": "MP short"}
                card_db.putsession("playerstats", "name",
                                   playview.p1name, "mp", remainingmp)
                # 対象ユニットHP減算
                api_common_common.unit_hp_change(
                    sid, playview, objcard2, value)

            elif re.match(pattern_p2leader, card2):
                # MP減算
                remainingmp = playview.p1mp - objcard1.cost
                if (remainingmp < 0):
                    return {"error": "MP short"}
                card_db.putsession("playerstats", "name",
                                   playview.p1name, "mp", remainingmp)
                # ALL OK DB更新
                card_db.appendlog(playview.playdata.card_table,
                                  "["+playview.p1name+"]spell:" + objcard1.name)
                card_db.appendlog(playview.playdata.card_table,
                                  "target->" + playview.p2name)
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
                if (newhp <= 0):
                    playview.playdata.gamewin(sid)
            else:
                return {"error": "illegal card2"}, 403

    # カード状態変更
    card_db.putsession(playview.playdata.card_table,
                       "cuid", objcard1.cuid,
                       "loc", playview.p1name + "_cemetery")

    return {"info": "OK"}
