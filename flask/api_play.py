import re

import api_common_status
import api_common_tension
import api_common_util
import card_db
from api_common_common import api_common_dmg, api_common_dmg_leader
from class_playinfo import Card_info
from class_playview import Play_view


def onplay_effect(sid, playview: Play_view, effect, card2, card3, isRun):
    # TODO 召喚時効果のバリエーション実装
    if "drow" in effect:
        if "bujutsu" in effect:
            playview.p1.draw_bujutsucard()
        elif "spell" in effect:
            playview.p1.draw_card_spell()
        else:
            playview.p1.draw_card()
        ret = "OK"
        scode = 200
    if "dmg" in effect:
        if not "leader" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                # 攻撃先確認
                pattern_p1board = r"leftboard_[0-5]$"  # 盤面
                pattern_p1leader = r"leftboard_"  # リーダー
                pattern_p2board = r"rightboard_[0-5]$"  # 盤面
                pattern_p2leader = r"rightboard_10"  # リーダー
                # TODO 自ボード、自リーダーへの攻撃
                if re.match(pattern_p2board, card3):
                    # ユニットHP減算
                    objcard3 = api_common_util.getobjcard(playview, card3)
                    if objcard3 is None:
                        return {"error": "unit don't exists in target card"}, 403
                    ret, scode = api_common_dmg(sid, playview, effect, objcard3)
                elif re.match(pattern_p2leader, card3):
                    # リーダーHP減算
                    ret, scode = api_common_dmg_leader(sid, playview, effect)
                else:
                    return {"error": "illegal target"}, 403
    if "attack" in effect:
        if "unit" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                ret, scode = api_common_status.api_common_attack(
                    sid, playview, effect, card3, isRun
                )
    if "tension" in effect:
        ret, scode = api_common_tension.api_common_tension(
            sid, playview, effect, card2, isRun
        )
    if "active" in effect:
        ret, scode = api_common_status.api_common_active(
            sid, playview, effect, card2, isRun
        )
    if "leader" in effect and "enemy" in effect:
        ret, scode = api_common_dmg(sid, playview, effect, "rightboard_10", isRun)
    return ret, scode


def api_play_hand(sid, playview: Play_view, card1, card2, card3):
    # ハンドからカードをプレイ
    pattern = r"[0-9]"
    number = int(re.findall(pattern, card1)[0])
    hands = playview.p1hand
    objcard1: Card_info
    objcard1 = hands[number]
    if objcard1 is None:
        return {"error": "illegal card1 number"}

    # ユニットの展開先確認
    pattern_p1board = r"leftboard_[0-5]"
    if re.match(pattern_p1board, card2):
        # ボードの確認
        pattern = r"[0-5]"
        number = int(re.findall(pattern, card2)[0])
        boards = playview.p1board
        objcard2 = boards[number]
        if objcard2 is not None:
            return {"error": "unit exists in card2"}
        # MP減算
        remainingmp = playview.p1mp - objcard1.cost
        if remainingmp < 0:
            return {"error": "MP short"}

        # 召喚時効果の確認
        ret = "OK"
        effect_array = objcard1.effect.split(",")
        effect: str
        for effect in effect_array:
            if effect.startswith("onplay"):
                ret, scode = onplay_effect(sid, playview, effect, card2, card3, False)

        if ret != "OK":
            return ret, scode

        # ALL OK DB更新
        card_db.appendlog(
            playview.playdata.card_table,
            "[" + playview.p1name + "]play:" + objcard1.name,
        )
        card_db.putsession("playerstats", "name", playview.p1name, "mp", remainingmp)
        card_db.putsession(
            playview.playdata.card_table,
            "cuid",
            objcard1.cuid,
            "loc",
            playview.p1name + "_board",
        )
        card_db.putsession(
            playview.playdata.card_table, "cuid", objcard1.cuid, "locnum", number
        )

        # 召喚時効果の実行
        for effect in effect_array:
            if effect.startswith("onplay"):
                ret, scode = onplay_effect(sid, playview, effect, card2, card3, True)

        playview = Play_view(sid)
        if playview.p1hp <= 0:
            playview.playdata.gameover(sid)
        if playview.p2hp <= 0:
            playview.playdata.gamewin(sid)
    else:
        return {"error": "illegal card2"}, 403

    return {"info": "OK"}
