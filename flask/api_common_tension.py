import re

import api_common_util
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_common_tension_objcard(
    sid,
    playview: Play_view,
    effect,
    objcard2: Card_info,
    isRun,
    player_self,
    player_enemy,
):
    if "tension" in effect:
        # 事前チェックは不要
        if not isRun:
            return "OK", 200
        pattern = r"[+-]?\d+"
        matches = re.search(pattern, effect)
        value = int(matches.group())
        if player_self is None:
            (
                board_self,
                board_enemy,
                player_self,
                player_enemy,
            ) = api_common_util.get_self_or_enemy(playview, objcard2)
        if "self" in effect or "each" in effect:
            newvalue = player_self.tension + value
            if newvalue > 3:
                newvalue = 3
            if isRun:
                card_db.putplayerstats(
                    "player_tid",
                    player_self.player_tid,
                    "tension",
                    newvalue,
                )
        if "enemy" in effect or "each" in effect:
            newvalue = player_enemy.tension + value
            if newvalue > 3:
                newvalue = 3
            if isRun:
                card_db.putplayerstats(
                    "player_tid",
                    player_enemy.player_tid,
                    "tension",
                    newvalue,
                )
    else:
        raise Exception

    return "OK", 200


def api_common_tension(sid, playview: Play_view, effect, card2: str, isRun):
    objcard2 = api_common_util.getobjcard(playview, card2)
    return api_common_tension_objcard(
        sid, playview, effect, objcard2, isRun, None, None
    )
