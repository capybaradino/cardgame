import random
import re

import api_common_common
import api_common_tension
import api_common_util
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def ondead(sid, playview: Play_view, objcard1: Card_info):
    effect_array = objcard1.effect.split(",")
    new_attack = objcard1.attack
    effect: str
    for effect in effect_array:
        if effect.startswith("ondead"):
            (
                board_self,
                board_enemy,
                player_self,
                player_enemy,
            ) = api_common_util.get_self_or_enemy(playview, objcard1)
            # TODO 死亡時効果のバリエーション実装
            # TODO 死亡時効果が範囲の場合
            if "tension" in effect:
                ret, scode = api_common_tension.api_common_tension_objcard(
                    sid, playview, effect, objcard1, True, player_self, player_enemy
                )
            if "dmg" in effect:
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
            if "drow" in effect:
                pattern = r"[+-]?\d+"
                matches = re.search(pattern, effect)
                value = int(matches.group())
                if "enemy" in effect:
                    i = 0
                    while i < value:
                        player_enemy.draw_card()
                        i = i + 1
                        card_db.appendlog(
                            playview.playdata.card_table, "draw->" + player_enemy.name
                        )
                if "self" in effect:
                    i = 0
                    while i < value:
                        player_self.draw_card_spell()
                        i = i + 1
                        card_db.appendlog(
                            playview.playdata.card_table, "draw->" + player_self.name
                        )

    return "OK", 200, new_attack
