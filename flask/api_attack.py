import re
from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def api_unit_attack(playview: Play_view, card1, card2):
    # ユニットで攻撃
    pattern = r'[0-9]'
    number = int(re.findall(pattern, card1)[0])
    boards = playview.p1board
    objcard1: Card_info
    objcard1 = boards[number]
    if(objcard1 is None):
        return {"error": "illegal card1 number"}
    # ユニットの攻撃先確認
    pattern_p2board = r'rightboard_[0-5]'
    if re.match(pattern_p2board, card2):
        # ボードの確認
        pattern = r'[0-5]'
        number = int(re.findall(pattern, card2)[0])
        boards = playview.p2board
        objcard2: Card_info
        objcard2 = boards[number]
        if(objcard2 is None):
            return {"error": "unit don't exists in card2"}
        # ALL OK DB更新
        # 自ユニットHP減算
        dhp = objcard1.dhp - objcard2.attack
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard1.cuid,
                           "dhp", dhp)
        if(objcard1.hp_org + dhp <= 0):
            card_db.putsession(playview.playdata.card_table,
                               "cuid", objcard1.cuid,
                               "loc", playview.p1name + "_cemetery")
        # 敵ユニットHP減算
        dhp = objcard2.dhp - objcard1.attack
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard2.cuid,
                           "dhp", dhp)
        if(objcard2.hp_org + dhp <= 0):
            card_db.putsession(playview.playdata.card_table,
                               "cuid", objcard2.cuid,
                               "loc", playview.p2name + "_cemetery")
    else:
        return {"error": "illegal card2"}
    
    return {"normal": "OK"}
