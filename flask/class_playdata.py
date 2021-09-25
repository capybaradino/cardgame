import card_db
import uuid
import card_util
import random


class Playdata:
    def __init__(self, sid) -> None:
        self.sid = sid
        self.gsid = card_db.getgsid_fromsid(sid)
        if(self.gsid != ""):
            gamesession = card_db.getgamesession(self.gsid)
        else:
            gamesession = None
        if(self.gsid == "" or gamesession is None):
            while True:
                gsid = str(uuid.uuid4())
                if(card_db.isexist_gsid(gsid)):
                    continue
                break
            cids = card_db.getallcids()
            num_cids = len(cids)
            p1_card0_ucid = cids[random.randrange(num_cids)][0]
            p2_card0_ucid = cids[random.randrange(num_cids)][0]
            p1_card0_status = ""
            p2_card0_status = ""
            self.log = "VS"
            lastupdate = card_util.card_getdatestrnow()
            card_db.postgamesession(
                self.gsid, p1_card0_ucid, p1_card0_status, p2_card0_ucid, p2_card0_status, self.log, lastupdate)
            card_db.putusersession_gsid(sid, gsid)
        else:
            p1_card0_ucid = gamesession[1]
            p1_card0_status = gamesession[2]
            p2_card0_ucid = gamesession[3]
            p2_card0_status = gamesession[4]
            self.log = gamesession[5]
            lastupdate = gamesession[6]
        self.p1_card0_filename = card_db.getfilename_fromcid(p1_card0_ucid)
        self.p2_card0_filename = card_db.getfilename_fromcid(p2_card0_ucid)
        self.p1_card0_cardname = card_db.getcardname_fromcid(p1_card0_ucid)
        self.p2_card0_cardname = card_db.getcardname_fromcid(p2_card0_ucid)

    def gameover(self):
        card_db.deletegamesession(self.gsid)
        card_db.putusersession_gsid(self.sid, '')
