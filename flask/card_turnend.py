import re

import api_common_common
import api_common_util
import card_db
from class_playdata import Playdata
from class_playinfo import Card_info
from class_playview import Play_view


def card_turnend(sid, state, nickname):
    playdata = Playdata(sid)
    if playdata.state != state:
        raise Exception
    # TODO ターン終了時処理
    playview = Play_view(sid)

    # 自ボードの処理
    data = card_db.getrecords_fromsession(
        playview.playdata.card_table, "loc", nickname + "_board"
    )
    boards = playview.p1board
    # 特定の列を基準にデータをソート
    column_index_to_sort = 3
    sorted_data = sorted(data, key=lambda x: x[column_index_to_sort])
    # ボードの処理
    for record in sorted_data:
        cuid = record[2]
        number = record[3]
        objcard2: Card_info
        objcard2 = boards[number]
        # ターン終了時効果(1回限り)
        turnend_effect_ontime = record[8]
        effect_array = turnend_effect_ontime.split(",")
        for effect in effect_array:
            if effect != "":
                api_common_common.apply_effect(
                    sid, playview, effect, objcard2, None, None, True
                )
        # 効果の削除
        card_db.putcardtable(
            playview.playdata.card_table,
            "cuid",
            objcard2.cuid,
            "turnend_effect_ontime",
            "",
        )
        # ターン終了時効果(永続)
        turnend_effect_static = record[7]
        effect_array = turnend_effect_static.split(",")
        for effect in effect_array:
            # TODO 自ボード対象キーワード
            if "onturnend_self" in effect:
                api_common_common.apply_effect(
                    sid, playview, effect, objcard2, None, None, True
                )

    # 相手ボードの処理
    data = card_db.getrecords_fromsession(
        playview.playdata.card_table, "loc", playview.p2name + "_board"
    )
    boards = playview.p2board
    # 特定の列を基準にデータをソート
    column_index_to_sort = 3
    sorted_data = sorted(data, key=lambda x: x[column_index_to_sort])
    # ボードの処理
    for record in sorted_data:
        cuid = record[2]
        number = record[3]
        objcard2: Card_info
        objcard2 = boards[number]
        # ターン終了時効果(1回限り)
        # ターン終了時効果(永続)
        turnend_effect_static = record[7]
        effect_array = turnend_effect_static.split(",")
        for effect in effect_array:
            # TODO 相手ボード対象キーワード
            if "onturnend_self_each" in effect:
                api_common_common.apply_effect(
                    sid, playview, effect, objcard2, None, None, True
                )

    if state == "p1turn":
        card_db.putgamesession(playdata.gsid, "state", "p2turn")
    else:
        card_db.putgamesession(playdata.gsid, "state", "p1turn")
    return
