import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_onattack_before(sid, playview: Play_view, objcard1):
    effect_array = objcard1.effect.split(",")
    new_attack = objcard1.attack
    for effect in effect_array:
        if effect.startswith("onattack"):
            # TODO 攻撃時効果のバリエーション実装
            if "attack" in effect:
                pattern = r"[+-]?\d+"
                matches = re.search(pattern, effect)
                value = int(matches.group())
                new_attack = objcard1.attack + value
            if "drow" in effect:
                # TODO mimic
                ret = "OK"

    return "OK", 200, new_attack
