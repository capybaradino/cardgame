import random
import re

import api_common_common
import api_common_status
import api_common_tension
import api_common_util
import card_db
from class_playdata import Player
from class_playinfo import Card_info
from class_playview import Play_view


def onplay_effect(sid, playview: Play_view, effect, card2, card3, isRun, objcard=None):
    return _onplay_effect(sid, playview, effect, card2, card3, objcard, isRun)


def onplay_effect_objcard(sid, playview: Play_view, effect, objcard: Card_info, isRun):
    return _onplay_effect(sid, playview, effect, None, None, objcard, isRun)


def onplay_effect_spell(
    sid, playview: Play_view, effect, objcard: Card_info, card2, isRun
):
    """効果の確認と実行(特技用)
    特技使用先(card2)は、内部関数上はcard3に変換する。
    (特技なので内部関数のcard2(ユニット配置先)は使わない)

    Args:
        sid (_type_): セッションID
        playview (Play_view): 引継ぎ情報
        effect (_type_): 効果(テキスト、単体)
        objcard (Card_info): 効果を発動するカードの情報
        card2 (_type_): 特技使用先の対象
        isRun (bool): 実行フラグ(事前チェックの場合はFalseにする)

    Returns:
        _type_: _description_
    """
    return _onplay_effect(sid, playview, effect, None, card2, objcard, isRun)


def _onplay_effect(
    sid, playview: Play_view, effect, card2, card3, objcard: Card_info, isRun
):
    """効果の確認と実行

    Args:
        sid (_type_): セッションID
        playview (Play_view): 引継ぎ情報
        effect (_type_): 効果(テキスト、単体)
        card2 (_type_): プレイ時のユニット配置先
        card3 (_type_): プレイ時または特技使用時の効果対象
        objcard (Card_info): 効果を発動するカードの情報
        isRun (bool): 実行フラグ(事前チェックの場合はFalseにする)

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    if objcard is not None:
        (
            board_self,
            board_enemy,
            player_self,
            player_enemy,
        ) = api_common_util.get_self_or_enemy(playview, objcard)
    # 特技無効チェック
    if card3 is not None:
        objcard3 = api_common_util.getobjcard(playview, card3)
        if objcard3 is not None:
            if "antieffect" in objcard3.status:
                return {"error": "target unit has antieffect"}, 403
    # 発動条件チェック
    if "onplay" in effect:
        # 正規表現でenemy_unit_Xoverにマッチするか確認(Xには数字が入る)
        pattern = r".*enemy_unit_[0-5]over.*"
        if re.match(pattern, effect):
            # effectをコロンで分割
            effect_array = effect.split(":")
            # 分割した1つ目の文字列のenemy_unit_XoverのXの部分を取り出す
            pattern = r"[0-5]"
            matches2 = re.search(pattern, effect_array[0])
            # Xの部分を数値に変換
            value = int(matches2.group())
            # 敵ユニットの数を数える
            i = 0
            for objcard2 in board_enemy:
                if objcard2 is not None:
                    i = i + 1
            # 敵ユニットの数がX以上か確認
            if i < value:
                # 発動しないがエラーにはしないで終了する
                return "OK", 200

    # TODO 効果のバリエーション実装
    if "switch" in effect:
        # 対象確認
        pattern_p1board = r"leftboard_[0-5]$"  # 盤面
        pattern_p2board = r"rightboard_[0-5]$"  # 盤面
        if re.match(pattern_p2board, card3) or re.match(pattern_p1board, card3):
            # TODO 対象制限の確認
            objcard2 = api_common_util.getobjcard(playview, card3)
            if objcard2 is None:
                return {"error": "unit don't exists in target card"}, 403
            # ALL OK DB更新
            if isRun:
                card_db.appendlog(
                    playview.playdata.card_table, "target->" + objcard2.name
                )
                # 対象ユニット場所入れ替え
                objcard3, loc1, loc2 = api_common_util.getobjcard_oppsite(
                    playview, card3
                )
                card_db.putdeck_locnum(
                    playview.playdata.card_table, objcard2.cuid, loc2
                )
                if objcard3 is not None:
                    card_db.putdeck_locnum(
                        playview.playdata.card_table, objcard3.cuid, loc1
                    )
        else:
            return {"error": "illegal target card"}, 403
        ret = "OK"
        scode = 200
    elif "draw" in effect:
        if isRun:
            if objcard is None:
                player = playview.p1
            else:
                if "enemy" in effect:
                    player = player_enemy
                else:
                    player = player_self
            pattern = r"[+-]?\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())
            i = 0
            while i < value:
                if "bujutsu" in effect:
                    player.draw_bujutsucard()
                elif "spell" in effect:
                    player.draw_card_spell()
                else:
                    player.draw_card()
                i = i + 1
        ret = "OK"
        scode = 200
    elif "dmg" in effect:
        if "random" in effect:
            pattern = r"[+-]?\d+"
            matches = re.search(pattern, effect)
            value = int(matches.group())
            if "enemy" in effect:
                index = []
                i = 0
                card: Card_info
                for card in board_enemy:
                    if card is not None:
                        # HP=0のユニットは除外
                        if card.hp_org + card.dhp > 0:
                            index.append(i)
                    i = i + 1
                leader = len(index)
                number = random.randrange(len(index) + 1)
                if number == leader:
                    card_db.appendlog(
                        playview.playdata.card_table, "effect->" + player_enemy.name
                    )
                    api_common_common.leader_hp_change(player_enemy, value)
                else:
                    objcard2 = board_enemy[index[number]]
                    card_db.appendlog(
                        playview.playdata.card_table, "effect->" + objcard2.name
                    )
                    api_common_common.unit_hp_change(sid, playview, objcard2, value)
                ret = "OK"
                scode = 200
            else:
                raise Exception("illegal randomdmg effect")
        elif "all" in effect:
            # 正規表現でXdmgにマッチする文字列を取り出す
            pattern = r"[0-5]dmg"
            matches = re.search(pattern, effect)
            # XdmgのXの部分を取り出す
            pattern = r"[0-5]"
            matches2 = re.search(pattern, matches.group())
            # Xの部分を数値に変換
            value = int(matches2.group())
            # 敵盤面ユニット全体にダメージ
            if "all_enemy_unit" in effect:
                # 敵盤面ユニット全体にダメージ
                objcard3s = []
                values = []
                for objcard2 in board_enemy:
                    if objcard2 is not None:
                        # HP=0のユニットは除外
                        if objcard2.hp_org + objcard2.dhp > 0:
                            objcard3s.append(objcard2)
                            values.append(value)
                # 対象ユニットが1つ以上いる場合はHP減算処理
                if len(objcard3s) > 0:
                    unit_hp_change_multi(sid, playview, objcard3s, values)
                ret = "OK"
                scode = 200

        elif "leader" in effect:
            # リーダーHP減算
            ret, scode = api_common_dmg_leader(sid, playview, effect, isRun)
        elif "any" in effect or "unit" in effect or "enemy" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                # 攻撃先確認
                pattern_p1board = r"leftboard_[0-5]$"  # 盤面
                pattern_p1leader = r"leftboard_"  # リーダー
                pattern_p2board = r"rightboard_[0-5]$"  # 盤面
                pattern_p2leader = r"rightboard_10"  # リーダー
                # TODO 自ボード、自リーダーへの攻撃
                if re.match(pattern_p2board, card3):
                    # 縦一列指定の場合
                    if "vertical" in effect:
                        # card3から数値を取り出す
                        pattern = r"[+-]?\d+"
                        matches = re.search(pattern, card3)
                        value = int(matches.group())
                        # 前列指定制限チェック
                        if "frontonly" in effect:
                            if value > 2:
                                return {"error": "target is not front"}, 403
                        # 対象ユニットHP減算
                        pattern = r"[+-]?\d+"
                        matches = re.search(pattern, effect)
                        value = int(matches.group())
                        objcard3s = []
                        values = []
                        i = 0
                        for objcard3tmp in playview.p2board:
                            if i > 2:
                                break
                            if objcard3tmp is not None:
                                objcard3s.append(objcard3tmp)
                                values.append(value)
                            i = i + i
                        # 対象ユニットが1つ以上いる場合はHP減算処理
                        if len(objcard3s) > 0:
                            unit_hp_change_multi(sid, playview, objcard3s, values)
                        ret = "OK"
                        scode = 200
                    # 単体指定の場合
                    else:
                        # ユニットHP減算
                        objcard3 = api_common_util.getobjcard(playview, card3)
                        if objcard3 is None:
                            return {"error": "unit don't exists in target"}, 403
                        # 前列指定制限チェック
                        if "frontonly" in effect:
                            if objcard3.locnum > 2:
                                return {"error": "target unit is not front"}, 403
                        if "times" in effect:
                            # unit_1dmg_3times というフォーマットの3の部分を取得
                            pattern = r"\d+(?!.*\d)"
                            matches = re.search(pattern, effect)
                            value = int(matches.group(0))
                            # effectから_3timesの部分を削除
                            effect = effect.replace(matches.group(0), "")
                        else:
                            value = 1
                        i = 0
                        while i < value:
                            ret, scode = api_common_dmg(
                                sid, playview, effect, objcard3, isRun
                            )
                            if ret == "HP0":
                                break
                            i = i + 1
                elif re.match(pattern_p2leader, card3):
                    # ユニット指定の場合はエラー
                    if "unit" in effect:
                        return {"error": "cannot target leader"}, 403
                    # リーダーHP減算
                    ret, scode = api_common_dmg_leader(sid, playview, effect, isRun)
                else:
                    return {"error": "illegal target"}, 403
        else:
            raise Exception("illegal dmg effect")
    elif "attack" in effect:
        if "unit" in effect:
            if card3 is None:
                return {"error": "Specify 3rd card"}, 403
            else:
                ret, scode = api_common_status.api_common_attack(
                    sid, playview, effect, card3, isRun
                )
        elif "self" in effect:
            # onattack専用
            api_common_status.api_common_attack_card(sid, playview, effect, objcard)
            ret = "OK"
            scode = 200

    elif "tension" in effect:
        if objcard is None:
            ret, scode = api_common_tension.api_common_tension(
                sid, playview, effect, card2, isRun
            )
        else:
            ret, scode = api_common_tension.api_common_tension_objcard(
                sid, playview, effect, objcard, isRun, player_self, player_enemy
            )
    elif "active" in effect:
        ret, scode = api_common_status.api_common_active(
            sid, playview, effect, card2, isRun
        )
    return ret, scode


def api_common_dmg(sid, playview: Play_view, effect, objcard2: Card_info, isRun):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # TODO 対象制限の確認
    ret = 1
    if isRun:
        # 対象ユニットHP減算
        card_db.appendlog(playview.playdata.card_table, "effect->" + objcard2.name)
        ret = api_common_common.unit_hp_change(sid, playview, objcard2, value)

    if ret <= 0:
        return "HP0", 200
    else:
        return "OK", 200


def api_common_dmg_leader(sid, playview: Play_view, effect, isRun):
    # HP変化系
    # TODO ターゲットフィルタ
    pattern = r"(^.*)_.*"
    matches = re.search(pattern, effect)
    target = matches.group(1)
    pattern = r"[+-]?\d+"
    matches = re.search(pattern, effect)
    value = int(matches.group())

    # TODO 対象制限の確認
    if isRun:
        # リーダーHP減算
        card_db.appendlog(playview.playdata.card_table, "effect->" + playview.p2name)
        api_common_common.leader_hp_change(playview.p2, value)

    return "OK", 200


def unit_hp_change_multi(sid, playview: Play_view, objcards, values):
    # 対象ユニットHP減算
    objcard2: Card_info
    i = 0
    for objcard2 in objcards:
        value = values[i]
        i = i + 1
        _unit_hp_change(sid, playview, objcard2, value, "hponly")
    # 死亡確認
    for objcard2 in objcards:
        _unit_hp_change(sid, playview, objcard2, 0, "deadonly")
    return


def unit_hp_change(sid, playview: Play_view, objcard2: Card_info, value):
    return _unit_hp_change(sid, playview, objcard2, value, "all")


def _unit_hp_change(sid, playview: Play_view, objcard2: Card_info, value, mode):
    """ユニットのHPを増減させる

    Args:
        playview (Play_view): Play_view
        objcard2 (Card_info): Card_info
        value (_type_): 増減させる値
        mode (str): "hponly" or "deadonly" or "all"
    """
    # 対象ユニットHP減算
    objcard2.refresh(playview.playdata.card_table)
    # メタルボディ
    if "metalbody" in objcard2.status:
        if value <= 3:
            value = 1
    if mode == "hponly" or mode == "all":
        objcard2.dhp = objcard2.dhp - value
        card_db.putsession(
            playview.playdata.card_table, "cuid", objcard2.cuid, "dhp", objcard2.dhp
        )
    else:
        objcard2.dhp = objcard2.dhp
    if objcard2.hp_org + objcard2.dhp <= 0 and (mode == "deadonly" or mode == "all"):
        (
            board_self,
            board_enemy,
            player_self,
            player_enemy,
        ) = api_common_util.get_self_or_enemy(playview, objcard2)
        card_db.putsession(
            playview.playdata.card_table,
            "cuid",
            objcard2.cuid,
            "loc",
            player_self.name + "_cemetery",
        )
        card_db.appendlog(playview.playdata.card_table, objcard2.name + " dead")
        # 死亡時効果発動
        _ondead_effect(sid, playview, objcard2)
    return objcard2.hp_org + objcard2.dhp


def _ondead_effect(sid, playview: Play_view, objcard2: Card_info):
    effect_array = objcard2.effect.split(",")
    for effect in effect_array:
        if effect.startswith("ondead"):
            # effectからondead:以外の部分を切り出し
            effectbody = objcard2.effect.split("ondead:")[1]
            api_common_common.onplay_effect_objcard(
                sid, playview, effectbody, objcard2, True
            )


def leader_hp_change(player: Player, value):
    """リーダーのHPを増減させる

    Args:
        player (Player): playview.p1/playview.p2 で指定推奨
        value (_type_): 増減させる値
    """
    # リーダーHP減算
    newhp = player.hp - value
    card_db.putsession("playerstats", "player_tid", player.player_tid, "hp", newhp)
    return
