import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db
import api_common_util
import api_common_status


def api_onattack(sid, playview: Play_view, objcard1: Card_info):
    effect_array = objcard1.effect.split(",")
    effect: str
    for effect in effect_array:
        if effect.startswith("onattack"):
            # TODO 攻撃時効果のバリエーション実装
            subeffect = effect.split(":")[1]
            if "attack" in subeffect:
                api_common_status.api_common_attack_card(
                    sid, playview, effect, objcard1)
            if "drow" in subeffect:
                if "enemy" in subeffect:
                    board_self, board_enemy, player_self, player_enemy = api_common_util.get_self_or_enemy(
                        playview, objcard1)
                    player_enemy.draw_card()
    # ステルス解除
    objcard1.refresh(playview.playdata.card_table)
    status = objcard1.status
    status = status.replace(",stealth", "")
    card_db.putsession(playview.playdata.card_table, "cuid",
                       objcard1.cuid, "status", status)

    return "OK", 200
