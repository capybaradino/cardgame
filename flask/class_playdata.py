import card_db
import uuid
import card_util
import random


class Player:
    def __init__(self, name, job, hp):
        self.name = name
        self.job = job
        self.hp = hp
        self.cards = []

    def __str__(self):
        return f"Name: {self.name}, Job: {self.job}"

    def take_damage(self, damage):
        self.health -= damage

    def add_card(self, card):
        if len(self.cards) < 30:
            self.cards.append(card)


class Playdata:
    def __init__(self, sid) -> None:
        self.sid = sid
        self.gsid = ""
        self.p1_player_table = ""
        self.p2_player_table = ""
        self.p1_card_table = ""
        self.p2_card_table = ""
        self.log = ""
        self.lastupdate = ""

        # 既存ゲームがあるか確認
        self.gsid = card_db.getgsid_fromsid(sid)
        if(self.gsid != ""):
            gamesession = card_db.getgamesession(self.gsid)
        else:
            gamesession = None

        # 新規ゲームの場合はテーブルを初期化
        if(self.gsid == "" or gamesession is None):
            while True:
                self.gsid = str(uuid.uuid4())
                if(card_db.isexist_gsid(self.gsid)):
                    continue
                break
            i = 0
            table = []
            while(i < 4):
                while True:
                    tablename = str(uuid.uuid4())
                    if(i < 2):
                        tablename = "p_" + tablename
                    else:
                        tablename = "c_" + tablename
                    if(card_db.is_table_exists(tablename)):
                        continue
                    break
                table.append(tablename)
                i = i + 1
            self.p1_player_table = table[0]
            self.p2_player_table = table[1]
            self.p1_card_table = table[2]
            self.p2_card_table = table[3]

            # cids = card_db.getallcids()
            # num_cids = len(cids)
            # player_card_ucid = cids[random.randrange(num_cids)][0]
            self.lastupdate = card_util.card_getdatestrnow()

            card_db.postgamesession(
                self.gsid, self.p1_player_table, self.p2_player_table,
                  self.p1_card_table, self.p2_card_table, self.log, self.lastupdate)
            card_db.putusersession_gsid(sid, self.gsid)
        else:
            self.p1_player_table = gamesession[1]
            self.p2_player_table = gamesession[2]
            self.p1_card_table = gamesession[3]
            self.p2_card_table = gamesession[4]
            self.log = gamesession[5]
            self.lastupdate = gamesession[6]

        # self.p1_card0_filename = card_db.getfilename_fromcid(p1_card0_ucid)
        # self.p2_card0_filename = card_db.getfilename_fromcid(p2_card0_ucid)
        # self.p1_card0_cardname = card_db.getcardname_fromcid(p1_card0_ucid)
        # self.p2_card0_cardname = card_db.getcardname_fromcid(p2_card0_ucid)

    def gameover(self):
        card_db.deletegamesession(self.gsid)
        card_db.putusersession_gsid(self.sid, '')
