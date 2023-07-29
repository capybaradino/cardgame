from flask.templating import render_template
from flask import redirect
from class_playdata import Playdata
import card_db


def card_createcardhtml(cuid):
    return


def card_createcardhtmlp2():
    filename = card_db.getfilename_fromupname("sleeve")
    text = "<img width=50 src='../uploads/"+filename+"'>"
    return text


class Card_view:
    def __init__(self, cid):
        self.cid = cid


class Play_view:
    def __init__(self, sid):
        playdata = Playdata(sid)
        p1=playdata.player1
        p2=playdata.player2
        # ヘッダ情報
        self.p1name = p1.name
        self.p2name = p2.name
        self.turnstate = playdata.state
        # Player2情報
        self.p2hp = p2.hp
        self.p2job = p2.job
        self.p2decknum = p2.get_decknum()
        self.p2mp = p2.mp
        self.p2maxmp = p2.maxmp
        self.p2tension = p2.tension
        # Player2ハンド
        # P2のハンドは枚数のみでスリーブ表示
        self.p2hand = []
        p2hands = p2.get_hand()
        i = 0
        while(i < 10):
            if(i < len(p2hands)):
                self.p2hand.append(Card_view(None))
            else:
                self.p2hand.append(None)
            i = i + 1
        # Player1盤面情報
        # Player2盤面情報
        # Player1情報
        self.p1hp = p1.hp
        self.p1job = p1.job
        self.p1decknum = p1.get_decknum()
        self.p1mp = p1.mp
        self.p1maxmp = p1.maxmp
        self.p1tension = p1.tension


def card_play_view(sid):
    playdata = Playdata(sid)

    if(playdata.stat == "lose"):
        return render_template(
            'play_lose.html', title='Lose'
        )

    viewdata = Play_view(sid)
    p1=playdata.player1
    p2=playdata.player2

    # ハンド
    i = 0
    p1hand = []
    p1hands = p1.get_hand()
    while(i < 10):
        if(i < len(p1hands)):
            cid = p1hands[i][0]
            filename = card_db.getfilename_fromcid(cid)
            cardname = card_db.getcardname_fromcid(cid)
            text = ""
            text = text + "<font color='Blue'>=1=</font><br>"
            text = text + "<img width=100 src='../uploads/"+filename+"'>"
            text = text + "<br>"+"<table width='100%' cellspacing='0' cellpadding='0'><tr>"
            text = text + "<td><font color='Red'>(1)</font></td>"
            text = text + "<td><div style='float: right;'><font color='Green'>(1)</font></div></td>"
            text = text + "</tr></table>"
            text = text + "<div style='text-align: center;'>"+cardname+"</div>"
            p1hand.append(text)
        else:
            p1hand.append(None)
        i = i + 1
    # P2のハンドは枚数のみでスリーブ表示
    p2hand = []
    p2hands = viewdata.p2hand
    for hand in p2hands:
        if(hand is not None):
            filename = card_db.getfilename_fromupname("sleeve")
            text = "<img width=50 src='../uploads/"+filename+"'>"
            p2hand.append(card_createcardhtmlp2())
        else:
            p2hand.append(None)
    
    # 盤面
    p1banmen = []
    i = 0
    while(i < 6):
        filename = card_db.getfilename_fromupname("land")
        p1banmen.append("../uploads/" + filename)
        i = i + 1
    p2banmen = []
    i = 0
    while(i < 6):
        filename = card_db.getfilename_fromupname("land")
        p2banmen.append("../uploads/" + filename)
        i = i + 1
    # 中央の空きマス
    filename = card_db.getfilename_fromupname("land")
    centercell = "../uploads/" + filename

    return render_template(
        'play.html', title='Play',
        p1_card=p1hand,
        p1_banmen=p1banmen,
        center_cell=centercell,
        p2_card=p2hand,
        p2_banmen=p2banmen,
        play_data=playdata,
        viewdata = viewdata
        )

def card_play_delete(sid, target, callback):
    playdata = Playdata(sid)
    playdata.gameover(sid)
    return redirect(callback)
    