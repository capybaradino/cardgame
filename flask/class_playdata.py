import card_db
import uuid
import card_util
import random


class Player:
    def __init__(self, name, job, hp, card_table):
        self.name = name
        self.job = job
        self.hp = hp
        self.card_table = card_table

    def __str__(self):
        return f"Name: {self.name}, Job: {self.job}"

    def draw_card(self):
        cuid = card_db.getfirstcuid_fromdeck(self.card_table, self.name)
        card_db.putdeck(self.card_table, cuid, self.name + "_hand")
        return
    
    def get_hand(self):
        return card_db.getcards_fromdeck(self.card_table, self.name + "_hand")

    def take_damage(self, damage):
        self.health -= damage


class Field:
    def __init__(self):
        self.land = []
    


class Playdata:
    def __init__(self, sid) -> None:
        self.gsid = ""
        self.p1_player_tid = ""
        self.p2_player_tid = ""
        self.card_table = ""
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
                # gsid生成
                self.gsid = str(uuid.uuid4())
                if(card_db.isexist_gsid(self.gsid)):
                    continue
                break
            i = 0
            table = []
            while(i < 3):
                while True:
                    name = str(uuid.uuid4())
                    if(i < 2):
                        # player_tid
                        name = "p_" + name
                    else:
                        # card_table
                        name = "c_" + name.replace('-','_')
                    if(card_db.is_table_exists(name)):
                        continue
                    break
                table.append(name)
                i = i + 1
            self.p1_player_tid = table[0]
            self.p2_player_tid = table[1]
            self.card_table = table[2]

            # ユーザ情報初期化
            self.player1 = Player(
                card_db.getnickname_fromsid(sid),
                "kensi",
                30,
                self.card_table
            )
            self.player2 = Player(
                "dummy",
                "kensi",
                30,
                self.card_table
            )
            card_db.postplayerstats(
                self.p1_player_tid, self.player1.name, self.player1.job, self.player1.hp)
            card_db.postplayerstats(
                self.p2_player_tid, self.player2.name, self.player2.job, self.player2.hp)

            # カード情報初期化
            card_db.createdecktable(self.card_table)

            cids = card_db.getallcids()
            num_cids = len(cids)
            # Player1デッキ登録(TBD)
            i = 0
            while(i < 30):
                tcid = cids[random.randrange(num_cids)][0]
                card_db.postdeck(self.card_table, tcid, self.player1.name)
                i = i + 1
            # Player2デッキ登録(TBD)
            i = 0
            while(i < 30):
                tcid = cids[random.randrange(num_cids)][0]
                card_db.postdeck(self.card_table, tcid, self.player2.name)
                i = i + 1

            # Player1ハンド
            self.player1.draw_card()
            self.player1.draw_card()
            self.player1.draw_card()
            # Player2ハンド
            self.player2.draw_card()
            self.player2.draw_card()
            self.player2.draw_card()

            # ゲームセッション登録
            self.lastupdate = card_util.card_getdatestrnow()
            card_db.postgamesession(
                self.gsid, self.p1_player_tid, self.p2_player_tid,
                  self.card_table, self.log, self.lastupdate)
            card_db.putusersession_gsid(sid, self.gsid)
        else:
            self.p1_player_tid = gamesession[1]
            self.p2_player_tid = gamesession[2]
            self.card_table = gamesession[3]
            self.log = gamesession[4]
            self.lastupdate = gamesession[5]

        self.p1_player_stats = card_db.getplayerstats(self.p1_player_tid)
        self.p2_player_stats = card_db.getplayerstats(self.p2_player_tid)
        self.player1 = Player(
            self.p1_player_stats[1],
            self.p1_player_stats[2],
            self.p1_player_stats[3],
            self.card_table
        )
        self.player2 = Player(
            self.p2_player_stats[1],
            self.p2_player_stats[2],
            self.p2_player_stats[3],
            self.card_table
        )

    def gameover(self):
        card_db.deletegamesession(self.gsid)
        card_db.putusersession_gsid(self.sid, '')
