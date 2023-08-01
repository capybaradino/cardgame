import card_db


class Card_info:
    def __init__(self, cid, cuid, locnum: int):
        self.cid = cid
        self.cuid = cuid
        self.locnum = locnum
        if(self.cid is not None):
            record = card_db.getrecord_fromgame("card_basicdata", "cid", cid)
            self.name = record[2]
            self.cost = record[5]
            self.category = record[6]
            self.attack = record[9]
            self.hp = record[10]
            self.effect = record[11]
            self.flavor = record[12]
            self.filename = card_db.getfilename_fromcid(self.cid)

