from class_playdata import Playdata
from class_playview import Play_view
import card_db
import re
from class_playinfo import Card_info


def card_turnend(sid, state, nickname):
    playdata = Playdata(sid)
    if (playdata.state != state):
        raise Exception
    # TODO ターン終了時処理
    playview = Play_view(sid)

    # 自ボードの処理
    data = card_db.getrecords_fromsession(
        playview.playdata.card_table, "loc", nickname + "_board")
    boards = playview.p1board
    # 特定の列を基準にデータをソート
    column_index_to_sort = 3
    sorted_data = sorted(data, key=lambda x: x[column_index_to_sort])
    # ボードの処理
    for record in sorted_data:
        cuid = record[2]
        number = record[3]
        turnend_effect_ontime = record[8]
        objcard2: Card_info
        objcard2 = boards[number]
        effect_array = turnend_effect_ontime.split(",")
        for effect in effect_array:
            if ("attack" in effect):
                pattern = r"[-+]?\d+"
                matches = re.search(pattern, effect)
                value = int(matches.group())
                # 対象ユニットステータス更新
                dattack = objcard2.dattack + value
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard2.cuid,
                                   "dattack", dattack)
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard2.cuid,
                           "turnend_effect_ontime", "")

    if (state == "p1turn"):
        card_db.putgamesession(playdata.gsid, "state", "p2turn")
    else:
        card_db.putgamesession(playdata.gsid, "state", "p1turn")
    return
