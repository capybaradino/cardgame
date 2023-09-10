from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def get_self_or_enemy(playview: Play_view, objcard1: Card_info):
    record = card_db.getrecord_fromsession(
        playview.playdata.card_table, "cuid", objcard1.cuid)
    loc: str
    loc = record[1]
    if (loc.startswith(playview.p1name)):
        board_self = playview.p1board
        board_enemy = playview.p2board
        if (playview.playdata.player1.name == playview.p1name):
            player_self = playview.playdata.player1
            player_enemy = playview.playdata.player2
        else:
            player_self = playview.playdata.player2
            player_enemy = playview.playdata.player1
    else:
        board_self = playview.p2board
        board_enemy = playview.p1board
        if (playview.playdata.player1.name == playview.p1name):
            player_self = playview.playdata.player2
            player_enemy = playview.playdata.player1
        else:
            player_self = playview.playdata.player1
            player_enemy = playview.playdata.player2
    return board_self, board_enemy, player_self, player_enemy
