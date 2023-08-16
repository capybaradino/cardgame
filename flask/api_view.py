from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def get(playview: Play_view):
    data_dict = {}
    # ターン
    data_dict["turn"] = playview.turnstate

    # Player1
    player1 = {}
    # 基本情報
    player1["name"] = playview.p1name
    player1["HP"] = playview.p1hp
    player1["decknum"] = playview.p1decknum
    player1["MP"] = playview.p1mp
    player1["maxMP"] = playview.p1maxmp
    player1["tension"] = playview.p1tension
    # ハンド
    p1hand = []
    handinfo: Card_info
    for handinfo in playview.p1hand:
        if (handinfo is not None):
            hand = {}
            hand["cost"] = handinfo.cost
            hand["attack"] = handinfo.attack
            hand["attack_org"] = handinfo.attack_org
            hand["hp"] = handinfo.hp
            hand["hp_org"] = handinfo.hp_org
            hand["graphic"] = "uploads/" + handinfo.filename
            p1hand.append(hand)
    player1["hand"] = p1hand
    # ボード
    p1board = []
    loc = 0
    boardinfo: Card_info
    for boardinfo in playview.p1board:
        if (boardinfo is not None):
            board = {}
            board["location"] = loc
            record = card_db.getrecord_fromsession(
                playview.playdata.card_table, "cuid", boardinfo.cuid)
            board["active"] = record[6]
            board["cost"] = boardinfo.cost
            board["attack"] = boardinfo.attack
            board["attack_org"] = boardinfo.attack_org
            board["hp"] = boardinfo.hp
            board["hp_org"] = boardinfo.hp_org
            board["graphic"] = "uploads/" + boardinfo.filename
            p1board.append(board)
        loc = loc + 1
    player1["board"] = p1board
    # Player1
    data_dict["player1"] = player1

    # Player2
    player2 = {}
    # 基本情報
    player2["name"] = playview.p2name
    player2["HP"] = playview.p2hp
    player2["decknum"] = playview.p2decknum
    player2["MP"] = playview.p2mp
    player2["maxMP"] = playview.p2maxmp
    player2["tension"] = playview.p2tension
    # Player2はハンドの中身は返さない
    player2["handnum"] = playview.p2handnum
    # ボード
    p2board = []
    loc = 0
    boardinfo: Card_info
    for boardinfo in playview.p2board:
        if (boardinfo is not None):
            board = {}
            board["location"] = loc
            board["cost"] = boardinfo.cost
            board["attack"] = boardinfo.attack
            board["attack_org"] = boardinfo.attack_org
            board["hp"] = boardinfo.hp
            board["hp_org"] = boardinfo.hp_org
            board["graphic"] = boardinfo.filename
            p2board.append(board)
        loc = loc + 1
    player2["board"] = p2board
    # Player1
    data_dict["player2"] = player2

    return data_dict


sample = {
    "turn": "player1",
    "player1": {
        "name": "Red",
        "HP": 30,
        "decknum": 30,
        "MP": 1,
        "maxMP": 1,
        "tension": 0,
        "hand": [
            {
                "cost": 1,
                "attack": 2,
                "hp": 3,
                "graphic": "hogehoge.png"
            }
        ],
        "board": [
            {
                "location": 0,
                "active": 1,
                "cost": 1,
                "attack": 2,
                "hp": 3,
                "graphic": "hogehoge.png"
            }
        ]
    },
    "player2": {
        "name": "Green",
        "HP": 30,
        "decknum": 30,
        "MP": 1,
        "maxMP": 1,
        "tension": 0,
        "handnum": 3,
        "board": [
            {
                "location": 0,
                "cost": 1,
                "attack": 2,
                "hp": 3,
                "graphic": "hogehoge.png"
            }
        ]
    }
}
