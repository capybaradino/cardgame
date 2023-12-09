import os

import card_db
import card_play_util
from class_playdata import Playdata
from class_playview import Play_view

from flask import redirect
from flask.templating import render_template


def card_play_get2(sid, param=None):
    playdata = Playdata(sid, param)
    isdebug = os.path.isfile("debug.conf")
    if isdebug:
        debug_code = '<h1><a href="../p1">(debug)Cardgame/p1</a></h1><h1><a href="../p2">(debug)Cardgame/p2</a></h1><h1><a href="../p3">(debug)Cardgame/p3</a></h1>'
    else:
        debug_code = ""

    if playdata.stat == "lose":
        return render_template("play_lose.html", title="Lose", debug_code=debug_code)

    if playdata.stat == "win":
        return render_template("play_win.html", title="Win", debug_code=debug_code)

    if playdata.stat == "matching":
        return render_template(
            "play_autoreload.html", title="Matching", msg="Match making..."
        )

    if playdata.stat == "cancel":
        return render_template("play_info.html", title="Cancel", msg="Match canceled.")

    if playdata.stat == "error":
        return render_template(
            "play_info.html",
            title="Error",
            msg="Error has occured. Go back and reload window.",
        )

    return render_template("play2.html")


def card_play_get(sid):
    playdata = Playdata(sid)
    isdebug = os.path.isfile("debug.conf")
    if isdebug:
        debug_code = '<h1><a href="../p1">(debug)Cardgame/p1</a></h1><h1><a href="../p2">(debug)Cardgame/p2</a></h1>'
    else:
        debug_code = ""

    if playdata.stat == "lose":
        return render_template("play_lose.html", title="Lose", debug_code=debug_code)

    if playdata.stat == "win":
        return render_template("play_win.html", title="Win", debug_code=debug_code)

    if playdata.stat == "matching":
        return render_template("play_matching.html", title="Matching")

    viewdata = Play_view(sid)

    # ハンド
    p1hand = []
    p1hands = viewdata.p1hand
    i = 0
    for hand in p1hands:
        if hand is not None:
            p1hand.append(card_play_util.card_createcardhtml(hand, "hand", i))
        else:
            p1hand.append(None)
        i = i + 1
    # P2のハンドは枚数のみでスリーブ表示
    p2hand = []
    p2hands = viewdata.p2hand
    for hand in p2hands:
        if hand is not None:
            p2hand.append(card_play_util.card_createcardhtmlp2())
        else:
            p2hand.append(None)

    # 盤面
    p1banmen = []
    i = 0
    while i < 6:
        p1banmen.append(card_play_util.card_createcardhtml(None, "p1board", i))
        i = i + 1
    for board in viewdata.p1board:
        if board is not None:
            i = board.locnum
            p1banmen[i] = card_play_util.card_createcardhtml(board, "p1board", i)
    p2banmen = []
    i = 0
    while i < 6:
        p2banmen.append(card_play_util.card_createcardhtml(None, "p2board", i))
        i = i + 1
    for board in viewdata.p2board:
        if board is not None:
            i = board.locnum
            p2banmen[i] = card_play_util.card_createcardhtml(board, "p2board", i)
    # プレイヤー
    p1name = card_play_util.card_radiobutton("p1board", 10)
    p2name = card_play_util.card_radiobutton("p2board", 10)
    # 中央の空きマス
    filename = card_db.getfilename_fromupname("land")
    centercell = "../uploads/" + filename

    # ターン情報
    if viewdata.turnstate == "p1turn":
        turnendbutton = (
            '<input type=button value="Turn end" onclick="system_turnend()">'
        )
    else:
        turnendbutton = ""

    return render_template(
        "play.html",
        title="Play",
        p1_card=p1hand,
        p1_banmen=p1banmen,
        p1_name=p1name,
        center_cell=centercell,
        p2_card=p2hand,
        p2_banmen=p2banmen,
        p2_name=p2name,
        play_data=playdata,
        viewdata=viewdata,
        turnendbutton=turnendbutton,
    )


def card_play_post(sid, target, callback):
    return redirect(callback)


def card_play_delete(sid, target, callback):
    playdata = Playdata(sid)
    playdata.gameover(sid)
    return redirect(callback)
