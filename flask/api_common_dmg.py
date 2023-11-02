import re

import api_common_common
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_common_dmg(sid, playview: Play_view, effect, objcard2: Card_info):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # TODO 対象制限の確認
    # 対象ユニットHP減算
    card_db.appendlog(playview.playdata.card_table, "effect->" + objcard2.name)
    api_common_common.unit_hp_change(sid, playview, objcard2, value)

    return "OK", 200


def api_common_dmg_leader(sid, playview: Play_view, effect):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # リーダーHP減算
    card_db.appendlog(playview.playdata.card_table, "effect->" + playview.p2name)
    api_common_common.leader_hp_change(playview.p2, value)

    return "OK", 200
