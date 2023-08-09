from class_playdata import Playdata
import card_db


def turnend(sid):
    playdata = Playdata(sid)
    nickname = card_db.getnickname_fromsid(sid)
    if(playdata.state == "p1turn"):
        if(nickname != playdata.player1.name):
            return 401
        card_db.putgamesession(playdata.gsid, "state", "p2turn")
        nextp = playdata.player2
    else:
        if(nickname != playdata.player2.name):
            return 401
        card_db.putgamesession(playdata.gsid, "state", "p1turn")
        nextp = playdata.player1
    nextp.start_turn()
    return 200
