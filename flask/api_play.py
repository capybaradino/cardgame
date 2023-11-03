import re

import card_db
from api_common_common import onplay_effect
from class_playinfo import Card_info
from class_playview import Play_view


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
        # MP減算確認
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
        # MP減算
        card_db.putsession("playerstats", "name", playview.p1name, "mp", remainingmp)
        # ハンドからボードへ移動
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
