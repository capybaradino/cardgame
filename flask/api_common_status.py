import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_common_attack(sid, playview: Play_view, effect, card2, isRun):
    if "attack" in effect:
        # ステータス変化系
        # TODO ターゲットフィルタ
        pattern = r"(^.*)_.*"
        matches = re.search(pattern, effect)
        target = matches.group(1)
        pattern = r"[+-]?\d+"
        matches = re.search(pattern, effect)
        value = int(matches.group())

        # 攻撃先確認
        pattern_p1board = r'leftboard_[0-5]$'   # 盤面
        pattern_p1leader = r'leftboard_10'  # リーダー
        pattern_p2board = r'rightboard_[0-5]$'   # 盤面
        pattern_p2leader = r'rightboard_10'  # リーダー
        # TODO 相手ボードへの効果
        if re.match(pattern_p1board, card2):
            # TODO 対象制限の確認

            # ボードの確認
            pattern = r'[0-5]'
            number = int(re.findall(pattern, card2)[0])
            boards = playview.p1board
            objcard2: Card_info
            objcard2 = boards[number]
            if (objcard2 is None):
                return {"error": "unit don't exists in target card"}, 403
            # ALL OK DB更新
            # 対象ユニットステータス更新
            dattack = objcard2.dattack + value
            if isRun:
                card_db.putsession(playview.playdata.card_table,
                                   "cuid", objcard2.cuid,
                                   "dattack", dattack)
            # このターンだけの場合減算をセット
            if ("thisturn" in effect):
                record = card_db.getrecord_fromsession(
                    playview.playdata.card_table, "cuid", objcard2.cuid)
                turnend_effect_ontime = record[8]
                turnend_effect_ontime = turnend_effect_ontime + ",attack-2"
                if isRun:
                    card_db.putsession(playview.playdata.card_table,
                                       "cuid", objcard2.cuid,
                                       "turnend_effect_ontime", turnend_effect_ontime)
    else:
        return {"error": "unit don't exists in target card"}, 403

    return "OK", 200
