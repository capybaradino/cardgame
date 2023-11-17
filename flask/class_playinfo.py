import re

import card_db


class Card_info:
    def __init__(self, cid, cuid, locnum: int, dhp: int, dattack: int):
        self.cid = cid
        self.cuid = cuid
        self.locnum = locnum
        self.dhp = dhp
        self.dattack = dattack
        if self.cid is not None:
            self.update()

    def update(self):
        record = card_db.getrecord_fromgame("card_basicdata", "cid", self.cid)
        self.name = record[2]
        self.cost = record[5]
        self.category = record[6]
        self.effect = record[11]
        self.flavor = record[12]
        if record[9] == "":
            self.attack_org = -1
        else:
            self.attack_org = record[9]
        if record[10] == "":
            self.hp_org = -1
        else:
            self.hp_org = record[10]
        # スキルブーストによるhp_org,attack_orgの変更
        if "skillboost" in self.effect:
            pattern = r"skillboost[+-]\d[+-]\d"
            matches = re.search(pattern, self.effect)
            # matchesから数値を取り出す
            pattern = r"[+-]\d"
            matches = re.findall(pattern, matches.group())
            boost_hp_ratio = int(matches[0])
            boost_attack_ratio = int(matches[1])
            # スキルブーストの値を取得
            record2 = card_db.getrecord_fromsession("playerstats", "name", self.name)
            skillboost = int(record2[7])
            # スキルブーストの値に応じてhp_org,attack_orgを変更
            self.dhp = self.dhp + boost_hp_ratio * skillboost
            self.dattack = self.dattack + boost_attack_ratio * skillboost

        self.attack = self.attack_org + self.dattack
        self.hp = self.hp_org + self.dhp
        pattern_session = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        fid = card_db.getfid_fromcid(self.cid)
        if re.match(pattern_session, fid):
            self.filename = card_db.getfilename_fromcid(self.cid)
        else:
            self.filename = fid

    def refresh(self, card_table: str):
        record = card_db.getrecord_fromsession(card_table, "cuid", self.cuid)
        self.locnum = record[3]
        self.dhp = record[4]
        self.dattack = record[5]
        self.status = record[9]
        self.update()

    @classmethod
    def empty(cls):
        return cls(None, None, None, None, None)
