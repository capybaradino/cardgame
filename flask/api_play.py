import re

from class_playinfo import Card_info
import card_db


def api_play_hand(playview, card1, card2):
    # ハンドからカードをプレイ
    pattern = r'[0-9]'
    number = int(re.findall(pattern, card1)[0])
    hands = playview.p1hand
    objcard1: Card_info
    objcard1 = hands[number]
    if (objcard1 is None):
        return {"error": "illegal card1 number"}
    # TODO ユニット以外の対応

    # ユニットの展開先確認
    pattern_p1board = r'leftboard_[0-5]'
    if re.match(pattern_p1board, card2):
        # ボードの確認
        pattern = r'[0-5]'
        number = int(re.findall(pattern, card2)[0])
        boards = playview.p1board
        objcard2 = boards[number]
        if (objcard2 is not None):
            return {"error": "unit exists in card2"}
        # MP減算
        remainingmp = playview.p1mp - objcard1.cost
        if (remainingmp < 0):
            return {"error": "MP short"}
        card_db.putsession("playerstats",
                           "name", playview.p1name,
                           "mp", remainingmp)
        # ALL OK DB更新
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard1.cuid,
                           "loc", playview.p1name + "_board")
        card_db.putsession(playview.playdata.card_table,
                           "cuid", objcard1.cuid,
                           "locnum", number)
    else:
        return {"error": "illegal card2"}

    return {"info": "OK"}
