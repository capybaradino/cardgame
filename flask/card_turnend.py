from class_playdata import Playdata
from class_playview import Play_view
import card_db
import re
from class_playinfo import Card_info
import api_common_util


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
        objcard2: Card_info
        objcard2 = boards[number]
        # ターン終了時効果(1回限り)
        turnend_effect_ontime = record[8]
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
        # ターン終了時効果(永続)
        turnend_effect_static = record[7]
        effect_array = turnend_effect_static.split(",")
        for effect in effect_array:
            # TODO 自ボード対象キーワード
            if ("onturnend_each" in effect):
                effect_detail = effect.split(":")[1]
                if ("1drow" in effect_detail):
                    board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
                        playview, objcard2)
                    player_self.draw_card()

    # 相手ボードの処理
    data = card_db.getrecords_fromsession(
        playview.playdata.card_table, "loc", playview.p2name + "_board")
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
            if ("onturnend_each" in effect):
                effect_detail = effect.split(":")[1]
                if ("1drow" in effect_detail):
                    board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
                        playview, objcard2)
                    player_enemy.draw_card()

    if (state == "p1turn"):
        card_db.putgamesession(playdata.gsid, "state", "p2turn")
    else:
        card_db.putgamesession(playdata.gsid, "state", "p1turn")
    return
