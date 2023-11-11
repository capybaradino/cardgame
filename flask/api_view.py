from class_playview import Play_view
from class_playinfo import Card_info
import card_db


def get(playview: Play_view):
    data_dict = {}
    # ターン
    data_dict["turn"] = playview.turnstate
    # ログ
    record = card_db.getrecord_fromsession(
        "gamesession", "card_table", playview.playdata.card_table
    )
    data_dict["log"] = record[4]

    # Player1
    player1 = {}
    # 基本情報
    player1["name"] = playview.p1name
    player1["HP"] = playview.p1hp
    player1["decknum"] = playview.p1decknum
    player1["MP"] = playview.p1mp
    player1["maxMP"] = playview.p1maxmp
    player1["tension"] = playview.p1tension
    player1["job"] = playview.p1job
    # テンションカードアクティブ確認
    record = card_db.getrecord_fromsession(
        playview.playdata.card_table, "loc", playview.p1name + "_tension"
    )
    active = record[6]
    player1["tension_active"] = active
    # ハンド
    p1hand = []
    handinfo: Card_info
    for handinfo in playview.p1hand:
        if handinfo is not None:
            hand = {}
            hand["cost"] = handinfo.cost
            hand["attack"] = handinfo.attack
            hand["attack_org"] = handinfo.attack_org
            hand["hp"] = handinfo.hp
            hand["hp_org"] = handinfo.hp_org
            hand["name"] = handinfo.name
            hand["graphic"] = "uploads/" + handinfo.filename
            hand["category"] = handinfo.category
            hand["effect"] = handinfo.effect
            p1hand.append(hand)
    player1["hand"] = p1hand
    # ボード
    p1board = []
    loc = 0
    boardinfo: Card_info
    for boardinfo in playview.p1board:
        if boardinfo is not None:
            board = {}
            board["location"] = loc
            record = card_db.getrecord_fromsession(
                playview.playdata.card_table, "cuid", boardinfo.cuid
            )
            board["active"] = record[6]
            board["cost"] = boardinfo.cost
            board["attack"] = boardinfo.attack
            board["attack_org"] = boardinfo.attack_org
            board["hp"] = boardinfo.hp
            board["hp_org"] = boardinfo.hp_org
            board["name"] = boardinfo.name
            board["graphic"] = "uploads/" + boardinfo.filename
            board["category"] = boardinfo.category
            board["effect"] = boardinfo.effect
            board["status"] = record[9]
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
    player2["job"] = playview.p2job
    # Player2はハンドの中身は返さない
    player2["handnum"] = playview.p2handnum
    # ボード
    p2board = []
    loc = 0
    boardinfo: Card_info
    for boardinfo in playview.p2board:
        if boardinfo is not None:
            board = {}
            board["location"] = loc
            record = card_db.getrecord_fromsession(
                playview.playdata.card_table, "cuid", boardinfo.cuid
            )
            board["cost"] = boardinfo.cost
            board["attack"] = boardinfo.attack
            board["attack_org"] = boardinfo.attack_org
            board["hp"] = boardinfo.hp
            board["hp_org"] = boardinfo.hp_org
            board["name"] = boardinfo.name
            board["graphic"] = "uploads/" + boardinfo.filename
            board["category"] = boardinfo.category
            board["effect"] = boardinfo.effect
            board["status"] = record[9]
            p2board.append(board)
        loc = loc + 1
    player2["board"] = p2board
    # Player1
    data_dict["player2"] = player2

    return data_dict
