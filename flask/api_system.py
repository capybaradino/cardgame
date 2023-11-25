import card_common
import card_db
import card_turnend
from class_playdata import Playdata


def surrender(sid):
    playdata = Playdata(sid)
    playdata.gameover(sid)
    return {"info": "OK"}


def turnend(sid):
    playdata = Playdata(sid)
    if playdata.stat == "win" or playdata.stat == "lose":
        return {"error": "game was over"}, 403
    nickname = card_db.getnickname_fromsid(sid)
    if playdata.state == "p1turn":
        if nickname != playdata.player1.name:
            return {"error": "illegal session or not your turn"}, 500
        card_turnend.card_turnend(sid, "p1turn", nickname)
        card_db.appendlog(playdata.card_table, "=" + nickname + " end=")
        nextp = playdata.player2
    else:
        if nickname != playdata.player2.name:
            return {"error": "illegal session or not your turn"}, 500
        card_turnend.card_turnend(sid, "p2turn", nickname)
        card_db.appendlog(playdata.card_table, "=" + nickname + " end=")
        nextp = playdata.player1
    nextp.start_turn()
    card_common.judge(sid)
    return {"info": "OK"}


def newgame(sid):
    playdata = Playdata(sid)
    return playdata.stat
