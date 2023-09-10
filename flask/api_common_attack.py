import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db
import api_common_util


def api_onattack_before(sid, playview: Play_view, objcard1: Card_info):
    effect_array = objcard1.effect.split(",")
    new_attack = objcard1.attack
    effect: str
    for effect in effect_array:
        if effect.startswith("onattack"):
            # TODO 攻撃時効果のバリエーション実装
            subeffect = effect.split(":")[1]
            if "attack" in subeffect:
                pattern = r"[+-]?\d+"
                matches = re.search(pattern, effect)
                value = int(matches.group())
                new_attack = objcard1.attack + value
            if "drow" in subeffect:
                if "enemy" in subeffect:
                    board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
                        playview, objcard1)
                    player_enemy.draw_card()

    return "OK", 200, new_attack
