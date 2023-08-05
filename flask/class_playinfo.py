import card_db


class Card_info:
    def __init__(self, cid, cuid, locnum: int, dhp: int, dattack: int):
        self.cid = cid
        self.cuid = cuid
        self.locnum = locnum
        self.dhp = dhp
        self.dattack = dattack
        if(self.cid is not None):
            record = card_db.getrecord_fromgame("card_basicdata", "cid", cid)
            self.name = record[2]
            self.cost = record[5]
            self.category = record[6]
            self.attack_org = record[9]
            self.hp_org = record[10]
            self.attack = record[9] + self.dattack
            self.hp = record[10] + self.dhp
            self.effect = record[11]
            self.flavor = record[12]
            self.filename = card_db.getfilename_fromcid(self.cid)

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None)

