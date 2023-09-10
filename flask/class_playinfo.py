import card_db
import re


class Card_info:
    def __init__(self, cid, cuid, locnum: int, dhp: int, dattack: int):
        self.cid = cid
        self.cuid = cuid
        self.locnum = locnum
        self.dhp = dhp
        self.dattack = dattack
        if (self.cid is not None):
            self.refresh()

    def refresh(self):
        record = card_db.getrecord_fromgame("card_basicdata", "cid", self.cid)
        self.name = record[2]
        self.cost = record[5]
        self.category = record[6]
        if record[9] == "":
            self.attack_org = -1
        else:
            self.attack_org = record[9]
        if record[10] == "":
            self.hp_org = -1
        else:
            self.hp_org = record[10]
        self.attack = self.attack_org + self.dattack
        self.hp = self.hp_org + self.dhp
        self.effect = record[11]
        self.flavor = record[12]
        pattern_session = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        fid = card_db.getfid_fromcid(self.cid)
        if re.match(pattern_session, fid):
            self.filename = card_db.getfilename_fromcid(self.cid)
        else:
            self.filename = fid

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None)
