import random
import re

import api_common_common
import api_common_status
import api_common_tension
import api_common_util
import card_db
from class_playdata import Player
from class_playinfo import Card_info
from class_playview import Play_view


def onplay_effect(sid, playview: Play_view, effect, card2, card3, isRun):
    return _onplay_effect(sid, playview, effect, card2, card3, None, isRun)


def onplay_effect_objcard(sid, playview: Play_view, effect, objcard: Card_info, isRun):
    return _onplay_effect(sid, playview, effect, None, None, objcard, isRun)


def _onplay_effect(
    sid, playview: Play_view, effect, card2, card3, objcard: Card_info, isRun
):
    if objcard is not None:
        (
            board_self,
            board_enemy,
            player_self,
            player_enemy,
        ) = api_common_util.get_self_or_enemy(playview, objcard)
    # TODO 召喚時効果のバリエーション実装
    if "drow" in effect:
        if isRun:
            if objcard is None:
                player = playview.p1
            else:
                if "enemy" in effect:
                    player = player_enemy
                else:
                    player = player_self
            pattern = r"[+-]?\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())
            i = 0
            while i < value:
                if "bujutsu" in effect:
                    player.draw_bujutsucard()
                elif "spell" in effect:
                    player.draw_card_spell()
                else:
                    player.draw_card()
                i = i + 1
        ret = "OK"
        scode = 200
    if "dmg" in effect:
        if "random" in effect:
            pattern = r"[+-]?\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())
            if "enemy" in effect:
                index = []
                i = 0
                card: Card_info
                for card in board_enemy:
                    if card is not None:
                        # HP=0のユニットは除外
                        if card.hp + card.dhp > 0:
                            index.append(i)
                    i = i + 1
                leader = len(index)
                number = random.randrange(len(index) + 1)
                if number == leader:
                    card_db.appendlog(
                        playview.playdata.card_table, "effect->" + player_enemy.name
                    )
                    api_common_common.leader_hp_change(player_enemy, value)
                else:
                    objcard2 = board_enemy[index[number]]
                    card_db.appendlog(
                        playview.playdata.card_table, "effect->" + objcard2.name
                    )
                    api_common_common.unit_hp_change(sid, playview, objcard2, value)
                ret = "OK"
                scode = 200
            else:
                raise Exception("illegal randomdmg effect")
        elif not "leader" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                # 攻撃先確認
                pattern_p1board = r"leftboard_[0-5]$"  # 盤面
                pattern_p1leader = r"leftboard_"  # リーダー
                pattern_p2board = r"rightboard_[0-5]$"  # 盤面
                pattern_p2leader = r"rightboard_10"  # リーダー
                # TODO 自ボード、自リーダーへの攻撃
                if re.match(pattern_p2board, card3):
                    # ユニットHP減算
                    objcard3 = api_common_util.getobjcard(playview, card3)
                    if objcard3 is None:
                        return {"error": "unit don't exists in target card"}, 403
                    ret, scode = api_common_dmg(sid, playview, effect, objcard3, isRun)
                elif re.match(pattern_p2leader, card3):
                    # リーダーHP減算
                    ret, scode = api_common_dmg_leader(sid, playview, effect, isRun)
                else:
                    return {"error": "illegal target"}, 403
        elif "leader" in effect:
            # リーダーHP減算
            ret, scode = api_common_dmg_leader(sid, playview, effect, isRun)
        else:
            raise Exception("illegal dmg effect")
    if "attack" in effect:
        if "unit" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                ret, scode = api_common_status.api_common_attack(
                    sid, playview, effect, card3, isRun
                )
    if "tension" in effect:
        if objcard is None:
            ret, scode = api_common_tension.api_common_tension(
                sid, playview, effect, card2, isRun
            )
        else:
            ret, scode = api_common_tension.api_common_tension_objcard(
                sid, playview, effect, objcard, isRun
            )
    if "active" in effect:
        ret, scode = api_common_status.api_common_active(
            sid, playview, effect, card2, isRun
        )
    return ret, scode


def api_common_dmg(sid, playview: Play_view, effect, objcard2: Card_info, isRun):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # TODO 対象制限の確認
    if isRun:
        # 対象ユニットHP減算
        card_db.appendlog(playview.playdata.card_table, "effect->" + objcard2.name)
        api_common_common.unit_hp_change(sid, playview, objcard2, value)

    return "OK", 200


def api_common_dmg_leader(sid, playview: Play_view, effect, isRun):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # TODO 対象制限の確認
    if isRun:
        # リーダーHP減算
        card_db.appendlog(playview.playdata.card_table, "effect->" + playview.p2name)
        api_common_common.leader_hp_change(playview.p2, value)

    return "OK", 200


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
        _ondead_effect(sid, playview, objcard2)
    return


def _ondead_effect(sid, playview: Play_view, objcard2: Card_info):
    effect_array = objcard2.effect.split(",")
    for effect in effect_array:
        if effect.startswith("ondead"):
            # effectからondead:以外の部分を切り出し
            effectbody = objcard2.effect.split("ondead:")[1]
            api_common_common.onplay_effect_objcard(
                sid, playview, effectbody, objcard2, True
            )


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
