import re

import api_common_util
import card_db
from class_playinfo import Card_info
from class_playview import Play_view


def api_common_active(sid, playview: Play_view, effect, card2, isRun):
    if "active" in effect:
        # 事前チェックは不要
        if not isRun:
            return "OK", 200
        objcard2 = api_common_util.getobjcard(playview, card2)
        (
            board_self,
            board_enemy,
            player_self,
            player_enemy,
        ) = api_common_util.get_self_or_enemy(playview, objcard2)
        if "self" in effect:
            if isRun:
                card_db.putcardtable(
                    playview.playdata.card_table, "cuid", objcard2.cuid, "active", 1
                )
    else:
        raise Exception

    return "OK", 200


def api_common_attack_card(sid, playview: Play_view, effect, objcard2: Card_info):
    if "attack" in effect:
        isRun = True
        # ステータス変化系
        # TODO ターゲットフィルタ
        # attack+-Xという文字列を正規表現で探して取得する
        pattern = r"attack[+-][0-9A-Z]+"
        matches = re.search(pattern, effect)
        target = matches.group()
        pattern = r"[+-]?\d+"
        matches = re.search(pattern, target)
        # 数値検索でヒットした場合はその値を使用
        if matches is not None:
            value = int(matches.group())
        else:
            # 数値検索でヒットしなかった場合はattack+の後ろの一文字を読み取る
            pattern = r"attack[+-](\w)"
            matches = re.search(pattern, effect)
            char = matches.group(1)
            # 文字がTであった場合は自分のテンション数を取得
            if char == "T":
                (
                    board_self,
                    board_enemy,
                    player_self,
                    player_enemy,
                ) = api_common_util.get_self_or_enemy(playview, objcard2)
                value = player_self.tension
            # 文字がAであった場合は相手のattackをゼロにする
            elif char == "A":
                value = -(objcard2.attack + objcard2.dattack)
            else:
                raise Exception

        if objcard2 is None:
            return {"error": "unit don't exists in target card"}, 403
        # ALL OK DB更新
        # 対象ユニットステータス更新
        dattack = objcard2.dattack + value
        if isRun:
            card_db.putcardtable(
                playview.playdata.card_table, "cuid", objcard2.cuid, "dattack", dattack
            )
        # このターンだけの場合減算をセット
        if "thisturn" in effect:
            record = card_db.getrecord_fromsession(
                playview.playdata.card_table, "cuid", objcard2.cuid
            )
            turnend_effect_ontime = record[8]
            turnend_effect_ontime = turnend_effect_ontime + ",self_attack-" + str(value)
            if isRun:
                card_db.putcardtable(
                    playview.playdata.card_table,
                    "cuid",
                    objcard2.cuid,
                    "turnend_effect_ontime",
                    turnend_effect_ontime,
                )
    else:
        return {"error": "unit don't exists in target card"}, 403

    return "OK", 200


def api_common_attack(sid, playview: Play_view, effect, card2, isRun):
    if "attack" in effect:
        # ステータス変化系
        # TODO ターゲットフィルタ

        # 攻撃先確認
        pattern_p1board = r"leftboard_[0-5]$"  # 盤面
        pattern_p1leader = r"leftboard_10"  # リーダー
        pattern_p2board = r"rightboard_[0-5]$"  # 盤面
        pattern_p2leader = r"rightboard_10"  # リーダー
        # 盤面を対象とする
        if re.match(pattern_p1board, card2):
            boards = playview.p1board
        elif re.match(pattern_p2board, card2):
            boards = playview.p2board
        else:
            return {"error": "unit don't exists in target card"}, 403

        # TODO 対象制限の確認
        # ボードの確認
        pattern = r"[0-5]"
        number = int(re.findall(pattern, card2)[0])
        objcard2: Card_info
        objcard2 = boards[number]
        if objcard2 is None:
            return {"error": "unit don't exists in target card"}, 403
        # ALL OK
        return api_common_attack_card(sid, playview, effect, objcard2)

    return "OK", 200
