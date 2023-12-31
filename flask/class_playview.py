import card_db
import card_util
from class_playdata import Field, Playdata
from class_playinfo import Card_info


class Play_view:
    def __init__(self, sid, timeoutcheck=False):
        self.sid = sid
        playdata = Playdata(sid, timeoutcheck=timeoutcheck)
        if playdata.stat == "timeout":
            return
        self.timeout = card_util.card_gettimeoutvalue()
        self.playdata = playdata
        nickname = card_db.getnickname_fromsid(sid)
        # ゲーム終了時のエラー対策
        if playdata.player1 is not None:
            if playdata.player1.name == nickname:
                p1 = playdata.player1
                p2 = playdata.player2
                self.turnstate = playdata.state
            else:
                p1 = playdata.player2
                p2 = playdata.player1
                if playdata.state == "p1turn":
                    self.turnstate = "p2turn"
                else:
                    self.turnstate = "p1turn"
            self.p1 = p1
            self.p2 = p2
            # ヘッダ情報
            self.p1name = p1.name
            self.p2name = p2.name
            # Player2情報
            self.p2hp = p2.hp
            self.p2job = p2.job
            self.p2decknum = p2.get_decknum()
            self.p2mp = p2.mp
            self.p2maxmp = p2.maxmp
            self.p2tension = p2.tension
            # Player2ハンド
            # P2のハンドは枚数のみでスリーブ表示
            self.p2hand = []
            p2hands = p2.get_hand()
            self.p2handnum = len(p2hands)
            i = 0
            while i < 10:
                if i < len(p2hands):
                    self.p2hand.append(Card_info.empty)
                else:
                    self.p2hand.append(None)
                i = i + 1
            # Player1盤面情報
            field = Field(self.p1name, self.p2name, playdata.card_table)
            self.p1board = []
            p1boards = field.get_p1board()
            i = 0
            while i < 6:
                self.p1board.append(None)
                for board in p1boards:
                    if i == board.locnum:
                        self.p1board[i] = board
                        break
                i = i + 1
            # Player2盤面情報
            field = Field(self.p1name, self.p2name, playdata.card_table)
            self.p2board = []
            p2boards = field.get_p2board()
            i = 0
            while i < 6:
                self.p2board.append(None)
                for board in p2boards:
                    if i == board.locnum:
                        self.p2board[i] = board
                        break
                i = i + 1
            # Player1情報
            self.p1hp = p1.hp
            self.p1job = p1.job
            self.p1decknum = p1.get_decknum()
            self.p1mp = p1.mp
            self.p1maxmp = p1.maxmp
            self.p1tension = p1.tension
            # Player1ハンド
            # P1のハンドは全情報表示
            self.p1hand = []
            p1hands = p1.get_hand()
            i = 0
            while i < 10:
                if i < len(p1hands):
                    self.p1hand.append(p1hands[i])
                else:
                    self.p1hand.append(None)
                i = i + 1

    def isblockable(self, board: Card_info):
        if board is not None:
            board.refresh()
            if "stealth" in board.status:
                return False
            else:
                return True
        else:
            return False

    def isblocked(self, number):
        # 前列に仁王立ちユニットがいる場合はブロックされる
        if self._hasfortress():
            # 自分が仁王立ちかつ前衛で無い場合に限る
            if not "fortress" in self.p2board[number].status:
                return True
            if number >= 3:
                return True
        # 前列にいる場合はブロックされない
        if number < 3:
            return False
        # 前にいるユニットがブロック可能か判定(ステルスはブロック不可)
        front = self.p2board[number - 3]
        if self.isblockable(front):
            return True
        else:
            return False

    def _hasfortress(self):
        i = 0
        for board in self.p2board:
            # 後列は対象外
            if i >= 3:
                break
            if board is not None:
                if "fortress" in board.status:
                    return True
        return False

    def iswall(self):
        # 上段
        upper1 = self.isblockable(self.p2board[0])
        upper2 = self.isblockable(self.p2board[3])
        # 中段
        middle1 = self.isblockable(self.p2board[1])
        middle2 = self.isblockable(self.p2board[4])
        # 下段
        lower1 = self.isblockable(self.p2board[2])
        lower2 = self.isblockable(self.p2board[5])

        if upper1 or upper2:
            if middle1 or middle2:
                if lower1 or lower2:
                    return True
        # ウォールが無くても仁王立ちがあればウォール扱い
        if self._hasfortress():
            return True
        return False
