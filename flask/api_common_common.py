from class_playview import Play_view
from class_playinfo import Card_info
from class_playdata import Player
import card_db
import api_common_dead
import api_common_util


def unit_hp_change_multi(sid, playview: Play_view, objcards, values):
    # 対象ユニットHP減算
    objcard2: Card_info
    i = 0
    for objcard2 in objcards:
        objcard2.refresh(playview.playdata.card_table)
        value = values[i]
        i = i + 1
        # メタルボディ
        if ("metalbody" in objcard2.status):
            if (value <= 3):
                value = 1
        dhp = objcard2.dhp - value
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard2.cuid,
                           "dhp", dhp)
    # 死亡確認
    for objcard2 in objcards:
        objcard2.refresh(playview.playdata.card_table)
        if (objcard2.hp <= 0):
            board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
                playview, objcard2)
            card_db.putsession(playview.playdata.card_table,
                               "cuid", objcard2.cuid,
                               "loc", player_self.name + "_cemetery")
            card_db.appendlog(playview.playdata.card_table,
                              objcard2.name + " dead")
            # 死亡時効果発動
            api_common_dead.ondead(sid, playview, objcard2)
    return


def unit_hp_change(sid, playview: Play_view, objcard2: Card_info, value):
    # 対象ユニットHP減算
    objcard2.refresh(playview.playdata.card_table)
    # メタルボディ
    if ("metalbody" in objcard2.status):
        if (value <= 3):
            value = 1
    dhp = objcard2.dhp - value
    card_db.putsession(playview.playdata.card_table,
                       "cuid", objcard2.cuid,
                       "dhp", dhp)
    if (objcard2.hp_org + dhp <= 0):
        board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
            playview, objcard2)
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard2.cuid,
                           "loc", player_self.name + "_cemetery")
        card_db.appendlog(playview.playdata.card_table,
                          objcard2.name + " dead")
        # 死亡時効果発動
        api_common_dead.ondead(sid, playview, objcard2)
    return


def leader_hp_change(playview: Play_view, player: Player, value):
    # リーダーHP減算
    newhp = player.hp - value
    card_db.putsession("playerstats",
                       "player_tid", player.player_tid,
                       "hp", newhp)
    return


def p2leader_hp_change(playview: Play_view, value):
    # リーダーHP減算
    newhp = playview.p2hp - value
    if (playview.playdata.player1.name == playview.p1name):
        card_db.putsession("playerstats",
                           "player_tid", playview.playdata.p2_player_tid,
                           "hp", newhp)
    else:
        card_db.putsession("playerstats",
                           "player_tid", playview.playdata.p1_player_tid,
                           "hp", newhp)
    return
