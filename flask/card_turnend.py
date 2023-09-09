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
    # ボードの処理
    data = card_db.getrecords_fromsession(
        playview.playdata.card_table, "loc", nickname + "_board")
    # 特定の列を基準にデータをソート
    column_index_to_sort = 3
    sorted_data = sorted(data, key=lambda x: x[column_index_to_sort])
    # ボードの処理
    for record in sorted_data:
        turnend_effect_ontime = record[8]
        effect_array = turnend_effect_ontime.split(",")
        number = record[3]
        for effect in effect_array:
            if ("attack" in effect):
                pattern = r"[-+]?\d+"
                matches = re.search(pattern, effect)
                value = int(matches.group())
                # 対象ユニットステータス更新
                boards = playview.p1board
                objcard2: Card_info
                objcard2 = boards[number]
                dattack = objcard2.dattack + value
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard2.cuid,
                                   "dattack", dattack)

    if (state == "p1turn"):
        card_db.putgamesession(playdata.gsid, "state", "p2turn")
    else:
        card_db.putgamesession(playdata.gsid, "state", "p1turn")
    return
