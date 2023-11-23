import re

import api_common_common
import api_common_status
import api_common_util
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_unit_attack(sid, playview: Play_view, card1, card2):
    # ユニットで攻撃
    pattern = r"[0-9]"
    number = int(re.findall(pattern, card1)[0])
    boards = playview.p1board
    objcard1: Card_info
    objcard1 = boards[number]
    if objcard1 is None:
        return {"error": "illegal card1 number"}, 403
    record = card_db.getrecord_fromsession(
        playview.playdata.card_table, "cuid", objcard1.cuid
    )
    if record[6] == 0:
        return {"error": "card1 is not active"}, 403
    # ユニットの攻撃先確認
    pattern_p2board = r"rightboard_[0-5]$"  # 盤面
    pattern_p2leader = r"rightboard_10"  # リーダー
    if re.match(pattern_p2board, card2):
        # ボードの確認
        pattern = r"[0-5]"
        number = int(re.findall(pattern, card2)[0])
        boards = playview.p2board
        objcard2: Card_info
        objcard2 = boards[number]
        if objcard2 is None:
            return {"error": "unit don't exists in card2"}, 403
        # ブロックの確認
        if playview.isblocked(number):
            return {"error": "card2 is blocked by other unit"}, 403
        # ステルスの確認
        objcard2.refresh()
        if "stealth" in objcard2.status:
            return {"error": "card2 has stealth"}, 403
        # 攻撃時効果
        ret = "OK"
        ret, scode = api_onattack(sid, playview, objcard1)
        objcard1.refresh()

        if ret != "OK":
            return ret, scode

        # ALL OK DB更新
        card_db.appendlog(
            playview.playdata.card_table,
            "[" + playview.p1name + "]attack:" + objcard1.name,
        )
        card_db.appendlog(playview.playdata.card_table, "target->" + objcard2.name)
        # HP減算ユニット登録(減算順)
        objcards = []
        objcards.append(objcard2)
        objcards.append(objcard1)
        values = []
        values.append(objcard1.attack)
        values.append(objcard2.attack)
        api_common_common.unit_hp_change_multi(sid, playview, objcards, values)
        # 自ユニットの行動回数を1減らす
        record = card_db.getrecord_fromsession(
            playview.playdata.card_table, "cuid", objcard1.cuid
        )
        nactive = int(record[6])
        card_db.putsession(
            playview.playdata.card_table, "cuid", objcard1.cuid, "active", nactive - 1
        )
    elif re.match(pattern_p2leader, card2):
        # ウォールのチェック
        if playview.iswall():
            return {"error": "wall exists"}, 403
        # 攻撃時効果
        ret = "OK"
        ret, scode = api_onattack(sid, playview, objcard1, ifleader=True)
        objcard1.refresh()

        if ret != "OK":
            return ret, scode

        # ALL OK DB更新
        card_db.appendlog(
            playview.playdata.card_table,
            "[" + playview.p1name + "]attack:" + objcard1.name,
        )
        card_db.appendlog(playview.playdata.card_table, "target->" + playview.p2name)
        # リーダーHP減算
        newhp = playview.p2hp - objcard1.attack
        if playview.playdata.player1.name == playview.p1name:
            card_db.putsession(
                "playerstats",
                "player_tid",
                playview.playdata.p2_player_tid,
                "hp",
                newhp,
            )
        else:
            card_db.putsession(
                "playerstats",
                "player_tid",
                playview.playdata.p1_player_tid,
                "hp",
                newhp,
            )
        # 自ユニットの行動回数を1減らす
        record = card_db.getrecord_fromsession(
            playview.playdata.card_table, "cuid", objcard1.cuid
        )
        nactive = int(record[6])
        card_db.putsession(
            playview.playdata.card_table, "cuid", objcard1.cuid, "active", nactive - 1
        )
        if newhp <= 0:
            playview.playdata.gamewin(sid)
    else:
        return {"error": "illegal card2"}, 403

    return {"info": "OK"}, 200


def api_onattack(sid, playview: Play_view, objcard1: Card_info, ifleader=False):
    effect_array = objcard1.effect.split(",")
    effect: str
    for effect in effect_array:
        if effect.startswith("onattack"):
            if effect.startswith("onattack_leader"):
                if not ifleader:
                    continue
            # 攻撃時効果
            subeffect = effect.split(":")[1]
            api_common_common.apply_effect(
                sid, playview, subeffect, objcard1, None, None, True
            )

    # ステルス解除
    objcard1.refresh()
    status = objcard1.status
    status = status.replace(",stealth", "")
    card_db.putsession(
        playview.playdata.card_table, "cuid", objcard1.cuid, "status", status
    )

    return "OK", 200
