from flask.templating import render_template
from flask import redirect
from class_playdata import Playdata
import card_db
from class_playview import Play_view
from class_playinfo import Card_info
import card_play_util


def card_play_get(sid):
    playdata = Playdata(sid)

    if(playdata.stat == "lose"):
        return render_template(
            'play_lose.html', title='Lose'
        )

    viewdata = Play_view(sid)
    p1=playdata.player1
    p2=playdata.player2

    # ハンド
    p1hand = []
    p1hands = viewdata.p1hand
    i = 0
    for hand in p1hands:
        if(hand is not None):
            p1hand.append(card_play_util.card_createcardhtml(hand, "p1_hand", i))
        else:
            p1hand.append(None)
        i = i + 1
    # P2のハンドは枚数のみでスリーブ表示
    p2hand = []
    p2hands = viewdata.p2hand
    for hand in p2hands:
        if(hand is not None):
            p2hand.append(card_play_util.card_createcardhtmlp2())
        else:
            p2hand.append(None)
    
    # 盤面
    p1banmen = []
    i = 0
    while(i < 6):
        p1banmen.append(card_play_util.card_createcardhtml(None, "p1_banmen", i))
        i = i + 1
    p2banmen = []
    i = 0
    while(i < 6):
        p2banmen.append(card_play_util.card_createcardhtml(None, "p2_banmen", i+10))
        i = i + 1
    # プレイヤー
    p1name = card_play_util.card_radiobutton("p1_banmen", 100)
    p2name = card_play_util.card_radiobutton("p2_banmen", 200)
    # 中央の空きマス
    filename = card_db.getfilename_fromupname("land")
    centercell = "../uploads/" + filename

    return render_template(
        'play.html', title='Play',
        p1_card=p1hand,
        p1_banmen=p1banmen,
        p1_name = p1name,
        center_cell=centercell,
        p2_card=p2hand,
        p2_banmen=p2banmen,
        p2_name = p2name,
        play_data=playdata,
        viewdata = viewdata
        )


def card_play_post(sid, target, callback):
    if(target=="turnend"):
        playdata = Playdata(sid)
        if(playdata.state == "p1turn"):
            card_db.putgamesession(playdata.gsid, "state", "p2turn")
            nextp = playdata.player2
        else:
            card_db.putgamesession(playdata.gsid, "state", "p1turn")
            nextp = playdata.player1
        nextp.start_turn()
    return redirect(callback)


def card_play_delete(sid, target, callback):
    playdata = Playdata(sid)
    playdata.gameover(sid)
    return redirect(callback)
    