import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_common_tension(sid, playview: Play_view, effect):
    if "tension" in effect:
        # TODO 片方のリーダー指定
        if "each" in effect:
            # 両リーダーテンション変化
            pattern = r"[+-]?\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())
            newvalue = playview.p1tension + value
            if (newvalue > 3):
                newvalue = 3
            card_db.putsession("playerstats",
                               "player_tid", playview.playdata.p1_player_tid,
                               "tension", newvalue)
            value = int(matches.group())
            newvalue = playview.p2tension + value
            if (newvalue > 3):
                newvalue = 3
            card_db.putsession("playerstats",
                               "player_tid", playview.playdata.p2_player_tid,
                               "tension", newvalue)
    else:
        raise Exception

    return "OK", 200
