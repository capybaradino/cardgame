import card_db
import uuid
import card_util
import random
from class_playinfo import Card_info
import game
import debug


class Player:
    def __init__(self, player_tid, name, job, hp, mp, maxmp, tension, card_table):
        self.player_tid = player_tid
        self.name = name
        self.job = job
        self.hp = hp
        self.mp = mp
        self.maxmp = maxmp
        self.tension = tension
        self.card_table = card_table
        self.hand = []

    def __str__(self):
        return f"Name: {self.name}, Job: {self.job}"

    def start_turn(self):
        self.draw_card()
        if (self.maxmp < 10):
            self.maxmp = self.maxmp + 1
        self.mp = self.maxmp
        card_db.putsession('playerstats', 'player_tid',
                           self.player_tid, 'mp', self.mp)
        card_db.putsession('playerstats', 'player_tid',
                           self.player_tid, 'maxmp', self.maxmp)
        card_db.putsession(self.card_table, "loc",
                           self.name+"_board", "active", 1)
        card_db.putsession(self.card_table, "loc",
                           self.name+"_tension", "active", 1)
        return

    def draw_card(self):
        cuid = card_db.getfirstcuid_fromdeck(self.card_table, self.name)
        if (len(self.get_hand()) < 10):
            card_db.putdeck(self.card_table, cuid, self.name + "_hand")
        else:
            card_db.putdeck(self.card_table, cuid, "drop")
        return

    def get_hand(self):
        records = card_db.getcards_fromdeck(
            self.card_table, self.name + "_hand")
        cards: Card_info = []
        for record in records:
            cards.append(
                Card_info(record[0], record[2], record[3], record[4], record[5]))
        return cards

    def get_decknum(self):
        deckcards = card_db.getcards_fromdeck(self.card_table, self.name)
        return len(deckcards)

    def take_damage(self, damage):
        self.health -= damage


class Field:
    def __init__(self, p1name, p2name, card_table):
        self.p1name = p1name
        self.p2name = p2name
        self.card_table = card_table
        self.board = []

    def get_p1board(self):
        records = card_db.getcards_fromdeck(
            self.card_table, self.p1name + "_board")
        cards: Card_info = []
        for record in records:
            cards.append(
                Card_info(record[0], record[2], record[3], record[4], record[5]))
        return cards

    def get_p2board(self):
        records = card_db.getcards_fromdeck(
            self.card_table, self.p2name + "_board")
        cards: Card_info = []
        for record in records:
            cards.append(
                Card_info(record[0], record[2], record[3], record[4], record[5]))
        return cards


class Playdata:
    def __init__(self, sid) -> None:
        self.gsid = ""
        self.p1_player_tid = ""
        self.p2_player_tid = ""
        self.card_table = ""
        self.log = ""
        self.lastupdate = ""
        self.stat = ""
        self.player1 = None
        self.player2 = None

        # 既存ゲームがあるか確認
        self.gsid = card_db.getgsid_fromsid(sid)
        if (self.gsid != ""):
            if (self.gsid == "lose"):
                self.stat = "lose"
                return
            elif (self.gsid == "win"):
                self.stat = "win"
                return
            else:
                gamesession = card_db.getgamesession(self.gsid)
        else:
            gamesession = None

        # 既存ゲームがあるか確認(2)
        record = card_db.getrecord_fromsession("playerstats",
                                               "name",
                                               card_db.getnickname_fromsid(sid))
        if (record is not None):
            player_tid = record[0]
            gamesession = card_db.getrecord_fromsession("gamesession",
                                                        "p1_player_tid",
                                                        player_tid)
            if (gamesession is not None):
                self.gsid = gamesession[0]
                card_db.putusersession_gsid(sid, self.gsid)
            else:
                gamesession = card_db.getrecord_fromsession("gamesession",
                                                            "p2_player_tid",
                                                            player_tid)
                if (gamesession is not None):
                    self.gsid = gamesession[0]
                    card_db.putusersession_gsid(sid, self.gsid)

        # 対戦待ちのゲームがあるか確認
        if (self.gsid == "" or gamesession is None):
            gamesession = card_db.getrecord_fromsession("gamesession",
                                                        "p2_player_tid",
                                                        "waiting")
            if (gamesession is not None):
                p1_player_tid = gamesession[1]
                record = card_db.getrecord_fromsession("playerstats",
                                                       "player_tid",
                                                       p1_player_tid)
                p1_player_name = record[1]
                if (p1_player_name == card_db.getnickname_fromsid(sid)):
                    # ゾンビゲームセッションがあった場合はつなぐ
                    self.gsid = gamesession[0]
                    card_db.putusersession_gsid(sid, self.gsid)
                    newgame = 0
                    matchinggame = 0
                else:
                    self.gsid = gamesession[0]
                    self.card_table = gamesession[3]
                    self.state = gamesession[5]
                    newgame = 0
                    matchinggame = 1
            else:
                newgame = 1
                matchinggame = 0
        else:
            newgame = 0
            matchinggame = 0

        # 新規ゲームの場合はテーブルを初期化
        if (newgame):
            while True:
                # gsid生成
                self.gsid = str(uuid.uuid4())
                if (card_db.isexist_gsid(self.gsid)):
                    continue
                break
            i = 0
            while True:
                # card_table生成
                name = str(uuid.uuid4())
                # card_table
                self.card_table = "c_" + name.replace('-', '_')
                if (card_db.is_table_exists(self.card_table)):
                    continue
                break

        if (newgame or matchinggame):
            while True:
                # player_tid生成
                name = str(uuid.uuid4())
                # player_tid
                name = "p_" + name
                if (card_db.isexist_player_tid(name)):
                    continue
                break
            if (newgame):
                self.p1_player_tid = name
            else:
                self.p2_player_tid = name

        # ゲーム設定値読み込み
        p1hp = int(game.getparam("p1hp"))
        p2hp = int(game.getparam("p2hp"))
        p1mp = int(game.getparam("p1mp"))
        p2mp = int(game.getparam("p2mp"))

        # ユーザ情報初期化
        if (newgame):
            self.player1 = Player(
                self.p1_player_tid,
                card_db.getnickname_fromsid(sid),
                "wiz",  # TODO 職業固定
                p1hp,
                p1mp,
                p1mp,
                0,
                self.card_table
            )
            card_db.postplayerstats(
                self.p1_player_tid, self.player1.name, self.player1.job,
                self.player1.hp, self.player1.mp, self.player1.maxmp, self.player1.tension)
        elif (matchinggame):
            if (self.state == "p1turn"):
                tension = 2
            else:
                tension = 0

            self.player2 = Player(
                self.p2_player_tid,
                card_db.getnickname_fromsid(sid),
                "wiz",
                p2hp,
                p2mp,
                p2mp,
                tension,
                self.card_table
            )
            card_db.postplayerstats(
                self.p2_player_tid, self.player2.name, self.player2.job,
                self.player2.hp, self.player2.mp, self.player2.maxmp, self.player2.tension)

        if (newgame):
            # カード情報初期化
            card_db.createdecktable(self.card_table)

        if (newgame or matchinggame):
            # デッキ登録(TODO)
            if (newgame):
                playername = self.player1.name
            else:
                playername = self.player2.name

            # TODO デッキ固定
            deck_name = "gamecard_2018haru_3_aguzesi"
            cids = card_db.getcids_fromdeck(deck_name)
            num_cids = len(cids)
            if (num_cids != 30):
                # TODO エラーケース
                return
            # 0から29までの数値を含むリストを作成
            numbers = list(range(30))
            # リストをランダムに並べ替える
            random.shuffle(numbers)
            i = 0
            while (i < 30):
                j = numbers[i]
                tcid = cids[j][0]
                card_db.postdeck(self.card_table, tcid, playername)
                i = i + 1

            # テンションカード登録
            tcid = "systemcid_tension"
            cuid = card_db.postdeck(self.card_table, tcid, playername)
            card_db.putdeck(self.card_table, cuid, playername + "_tension")

        if (newgame):
            # Player1ハンド
            self.player1.draw_card()
            self.player1.draw_card()
            self.player1.draw_card()
        elif (matchinggame):
            # Player2ハンド
            self.player2.draw_card()
            self.player2.draw_card()
            self.player2.draw_card()

        if (newgame):
            # Player先行後攻コイントス
            ret = debug.getdebugparam("senkou")
            if (ret is None):
                ret = str(random.randrange(2))
            if (ret == "0"):
                # self.player1.start_turn()
                self.state = "p1turn"
                self.player1.start_turn()
            else:
                # self.player2.start_turn()
                self.state = "p2turn"
                card_db.putsession("playerstats", "name",
                                   self.player1.name, "tension", 2)

            # ゲームセッション登録
            self.lastupdate = card_util.card_getdatestrnow()
            card_db.postgamesession(
                self.gsid, self.p1_player_tid, "waiting",
                self.card_table, self.log, self.state, self.lastupdate)
            card_db.putusersession_gsid(sid, self.gsid)
        elif (matchinggame):
            # マッチング完了登録
            card_db.putgamesession(self.gsid, "p2_player_tid",
                                   self.p2_player_tid)
            card_db.putusersession_gsid(sid, self.gsid)
            if (self.state == "p2turn"):
                self.player2.start_turn()

        # マッチング中・・・
        i = 0
        gamesession = card_db.getgamesession(self.gsid)
        self.p2_player_tid = gamesession[2]
        if (self.p2_player_tid == "waiting"):
            self.stat = "matching"
            self.card_table = gamesession[3]
            return

        self.p1_player_tid = gamesession[1]
        self.p2_player_tid = gamesession[2]
        self.card_table = gamesession[3]
        self.log = gamesession[4]
        self.state = gamesession[5]
        self.lastupdate = gamesession[6]

        self.p1_player_stats = card_db.getplayerstats(self.p1_player_tid)
        self.p2_player_stats = card_db.getplayerstats(self.p2_player_tid)
        self.player1 = Player(
            self.p1_player_stats[0],
            self.p1_player_stats[1],
            self.p1_player_stats[2],
            self.p1_player_stats[3],
            self.p1_player_stats[4],
            self.p1_player_stats[5],
            self.p1_player_stats[6],
            self.card_table
        )
        self.player2 = Player(
            self.p2_player_stats[0],
            self.p2_player_stats[1],
            self.p2_player_stats[2],
            self.p2_player_stats[3],
            self.p2_player_stats[4],
            self.p2_player_stats[5],
            self.p2_player_stats[6],
            self.card_table
        )
        return

    def cleargame(self, sid, iswin):
        # 要求されたゲームの処理
        card_db.deletedecktable(self.card_table)
        card_db.deleteplayerstats(self.p1_player_tid)
        card_db.deleteplayerstats(self.p2_player_tid)
        card_db.deletegamesession(self.gsid)
        gsid = card_db.getgsid_fromsid(sid)
        if (iswin == "win"):
            result1 = "win"
            result2 = "lose"
        else:
            result1 = "lose"
            result2 = "win"
        card_db.putusersession_gsid(sid, result1)
        sid2 = card_db.getsid_fromgsid(gsid)
        if (sid2 is not None):
            card_db.putusersession_gsid(sid2, result2)
        # ゾンビセッションの整理
        name = card_db.getnickname_fromsid(sid)
        while True:
            record = card_db.getrecord_fromsession("playerstats", "name", name)
            if record is None:
                break
            player_tid = record[0]
            record = card_db.getrecord_fromsession(
                "gamesession", "p1_player_tid", player_tid)
            if record is not None:
                card_table = record[3]
                other_player_tid = record[2]
                gsid = record[0]
                card_db.deletedecktable(card_table)
                card_db.deleteplayerstats(other_player_tid)
                card_db.deletegamesession(gsid)
            card_db.deleteplayerstats(player_tid)
        return

    def gamewin(self, sid):
        self.cleargame(sid, 'win')

    def gameover(self, sid):
        self.cleargame(sid, 'lose')
