import re

import api_common_common
import api_common_util
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_spell(sid, playview: Play_view, card1, card2):
    # 特技使用
    pattern = r"[0-9]"
    number = int(re.findall(pattern, card1)[0])
    hands = playview.p1hand
    objcard1: Card_info
    objcard1 = hands[number]
    if objcard1 is None:
        return {"error": "illegal card1 number"}, 403

    # TODO 多種特技の内容対応
    effect_array = objcard1.effect.split(",")
    # 特技の対象確認
    for effect in effect_array:
        # 事前チェック
        ret, scode = api_common_common.onplay_effect_spell(
            sid, playview, effect, objcard1, card2, False
        )
        if ret != "OK":
            return ret, scode

        # MP減算確認
        remainingmp = playview.p1mp - objcard1.cost
        if remainingmp < 0:
            return {"error": "MP short"}, 403

        # ALL OK DB更新
        # 監査ログ
        card_db.appendlog(
            playview.playdata.card_table,
            "[" + playview.p1name + "]spell:" + objcard1.name,
        )
        # MP減算
        card_db.putsession("playerstats", "name", playview.p1name, "mp", remainingmp)
        ret, scode = api_common_common.onplay_effect_spell(
            sid, playview, effect, objcard1, card2, True
        )

    # カード状態変更
    card_db.putsession(
        playview.playdata.card_table,
        "cuid",
        objcard1.cuid,
        "loc",
        playview.p1name + "_cemetery",
    )

    return {"info": "OK"}, 200
