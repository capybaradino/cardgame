import re

import api_common_common
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_tension(sid, playview: Play_view, card1, card2):
    # テンション・テンションスキル
    # テンション値確認
    tension = playview.p1tension
    if tension < 3:
        # テンションアップ
        # テンションカードアクティブ確認
        record = card_db.getrecord_fromsession(
            playview.playdata.card_table, "loc", playview.p1name + "_tension"
        )
        cuid = record[2]
        active = record[6]
        if active == 0:
            return {"error": "Tension not active"}
        # MP減算
        remainingmp = playview.p1mp - 1
        if remainingmp < 0:
            return {"error": "MP short"}
        card_db.putplayerstats("name", playview.p1name, "mp", remainingmp)
        tension = tension + 1
        card_db.putplayerstats("name", playview.p1name, "tension", tension)
        # テンションカードを非アクティブ化
        card_db.putcardtable(playview.playdata.card_table, "cuid", cuid, "active", 0)
        card_db.appendlog(
            playview.playdata.card_table, "[" + playview.p1name + "]tension up:"
        )
    else:
        # テンションスキル発動
        # ジョブ確認
        job = playview.p1job

        # 武闘家
        if job == "mnk":
            playview.p1.draw_card()
            playview.p1.draw_bujutsucard()
            # ALL OK DB更新
            card_db.appendlog(
                playview.playdata.card_table, "[" + playview.p1name + "]tension skill:"
            )
        # 魔法使い
        elif job == "wiz":
            # 事前チェック
            ret, scode = api_common_common.apply_effect(
                sid, playview, "any_3dmg", None, None, card2, False
            )
            if ret != "OK":
                return ret, scode
            # ALL OK DB更新
            card_db.appendlog(
                playview.playdata.card_table,
                "[" + playview.p1name + "]tension skill:",
            )
            _reset_tension(playview)
            api_common_common.apply_effect(
                sid, playview, "any_3dmg", None, None, card2, True
            )
            # 勝敗確認
            playview = Play_view(sid)
            if playview.p1hp <= 0:
                playview.playdata.gameover(sid)
            if playview.p2hp <= 0:
                playview.playdata.gamewin(sid)
            return {"info": "OK"}

        else:
            return {"error": "unknown job"}, 403

        # テンション初期化
        _reset_tension(playview)

    return {"info": "OK"}


def _reset_tension(playview):
    # テンション初期化
    card_db.putplayerstats("name", playview.p1name, "tension", 0)
    # スキルブースト+1
    record = card_db.getplayerstats_byname(playview.p1name)
    skillboost = record[7]
    skillboost = skillboost + 1
    card_db.putplayerstats("name", playview.p1name, "skillboost", skillboost)
    return
