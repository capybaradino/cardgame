import api_common_dead
import api_common_util
import card_db
from class_playdata import Player
from class_playinfo import Card_info
from class_playview import Play_view


def unit_hp_change_multi(sid, playview: Play_view, objcards, values):
    # 対象ユニットHP減算
    objcard2: Card_info
    i = 0
    for objcard2 in objcards:
        value = values[i]
        i = i + 1
        _unit_hp_change(sid, playview, objcard2, value, "hponly")
    # 死亡確認
    for objcard2 in objcards:
        _unit_hp_change(sid, playview, objcard2, 0, "deadonly")
    return


def unit_hp_change(sid, playview: Play_view, objcard2: Card_info, value):
    _unit_hp_change(sid, playview, objcard2, value, "all")


def _unit_hp_change(sid, playview: Play_view, objcard2: Card_info, value, mode):
    """ユニットのHPを増減させる

    Args:
        playview (Play_view): Play_view
        objcard2 (Card_info): Card_info
        value (_type_): 増減させる値
        mode (str): "hponly" or "deadonly" or "all"
    """
    # 対象ユニットHP減算
    objcard2.refresh(playview.playdata.card_table)
    # メタルボディ
    if "metalbody" in objcard2.status:
        if value <= 3:
            value = 1
    if mode == "hponly" or mode == "all":
        objcard2.dhp = objcard2.dhp - value
        card_db.putsession(
            playview.playdata.card_table, "cuid", objcard2.cuid, "dhp", objcard2.dhp
        )
    else:
        objcard2.dhp = objcard2.dhp
    if objcard2.hp_org + objcard2.dhp <= 0 and (mode == "deadonly" or mode == "all"):
        (
            board_self,
            board_enemy,
            player_self,
            player_enemy,
        ) = api_common_util.get_self_or_enemy(playview, objcard2)
        card_db.putsession(
            playview.playdata.card_table,
            "cuid",
            objcard2.cuid,
            "loc",
            player_self.name + "_cemetery",
        )
        card_db.appendlog(playview.playdata.card_table, objcard2.name + " dead")
        # 死亡時効果発動
        api_common_dead.ondead(sid, playview, objcard2)
    return


def leader_hp_change(player: Player, value):
    """リーダーのHPを増減させる

    Args:
        player (Player): playview.p1/playview.p2 で指定推奨
        value (_type_): 増減させる値
    """
    # リーダーHP減算
    newhp = player.hp - value
    card_db.putsession("playerstats", "player_tid", player.player_tid, "hp", newhp)
    return
