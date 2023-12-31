import re

import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def getobjcard_oppsite(playview_in: Play_view, card2: str):
    # refresh
    playview = Play_view(playview_in.sid)
    # ボードの確認
    pattern = r"[0-5]"
    number = int(re.findall(pattern, card2)[0])
    if number < 3:
        number2 = number + 3
    else:
        number2 = number - 3
    if card2.startswith("left"):
        boards = playview.p1board
    else:
        boards = playview.p2board
    objcard2: Card_info
    objcard2 = boards[number2]
    if objcard2 is not None:
        objcard2.refresh()
    return objcard2, number, number2


def getobjcard(playview_in: Play_view, card2: str):
    # refresh
    playview = Play_view(playview_in.sid)
    # ボードの確認
    pattern = r"[0-5]"
    number = int(re.findall(pattern, card2)[0])
    if card2.startswith("left"):
        boards = playview.p1board
    else:
        boards = playview.p2board
    objcard2: Card_info
    objcard2 = boards[number]
    if objcard2 is not None:
        objcard2.refresh()
    return objcard2


def get_self_or_enemy(playview_in: Play_view, objcard1: Card_info):
    # refresh
    playview = Play_view(playview_in.sid)
    record = card_db.getrecord_fromsession(
        playview.playdata.card_table, "cuid", objcard1.cuid
    )
    loc: str
    loc = record[1]
    if loc.startswith(playview.p1name):
        board_self = playview.p1board
        board_enemy = playview.p2board
        if playview.playdata.player1.name == playview.p1name:
            player_self = playview.playdata.player1
            player_enemy = playview.playdata.player2
        else:
            player_self = playview.playdata.player2
            player_enemy = playview.playdata.player1
    else:
        board_self = playview.p2board
        board_enemy = playview.p1board
        if playview.playdata.player1.name == playview.p1name:
            player_self = playview.playdata.player2
            player_enemy = playview.playdata.player1
        else:
            player_self = playview.playdata.player1
            player_enemy = playview.playdata.player2
    return board_self, board_enemy, player_self, player_enemy
