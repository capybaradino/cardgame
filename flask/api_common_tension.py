import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db
import api_common_util


def api_common_tension(sid, playview: Play_view, effect, card2: str, isRun):
    if "tension" in effect:
        # 事前チェックは不要
        if not isRun:
            return "OK", 200
        pattern = r"[+-]?\d+"
        matches = re.search(pattern, effect)
        value = int(matches.group())
        objcard2 = api_common_util.getobjcard(playview, card2)
        board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
            playview, objcard2)
        if "self" in effect or "each" in effect:
            newvalue = playview.p1tension + value
            if (newvalue > 3):
                newvalue = 3
            if isRun:
                card_db.putsession("playerstats",
                                   "player_tid", player_self.player_tid,
                                   "tension", newvalue)
        if "enemy" in effect or "each" in effect:
            newvalue = playview.p2tension + value
            if (newvalue > 3):
                newvalue = 3
            if isRun:
                card_db.putsession("playerstats",
                                   "player_tid", player_enemy.player_tid,
                                   "tension", newvalue)
    else:
        raise Exception

    return "OK", 200
