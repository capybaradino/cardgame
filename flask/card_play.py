from flask.templating import render_template
from flask import redirect
from class_playdata import Playdata
import card_db


def card_play_view(sid):
    playdata = Playdata(sid)

    if(playdata.stat == "lose"):
        return render_template(
            'play_lose.html', title='Lose'
        )

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
    p2hands = p2.get_hand()
    i = 0
    while(i < 10):
        if(i < len(p2hands)):
            filename = card_db.getfilename_fromupname("sleeve")
            text = "<img width=50 src='../uploads/"+filename+"'>"
            p2hand.append(text)
        else:
            p2hand.append(None)
        i = i + 1
    
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
        p1_name=p1.name, p1_hp=p1.hp,
        p1_card=p1hand,
        p1_banmen=p1banmen,
        center_cell=centercell,
        p2_name=p2.name, p2_hp=p2.hp,
        p2_card=p2hand,
        p2_banmen=p2banmen,
        play_data=playdata,
        card_db=card_db
        )

def card_play_delete(sid, target, callback):
    playdata = Playdata(sid)
    playdata.gameover(sid)
    return redirect(callback)
    