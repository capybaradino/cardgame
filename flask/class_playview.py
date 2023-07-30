import card_db
from class_playdata import Playdata
from class_playinfo import Card_info


class Play_view:
    def __init__(self, sid):
        playdata = Playdata(sid)
        p1=playdata.player1
        p2=playdata.player2
        # ヘッダ情報
        self.p1name = p1.name
        self.p2name = p2.name
        self.turnstate = playdata.state
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
        i = 0
        while(i < 10):
            if(i < len(p2hands)):
                self.p2hand.append(Card_info(None, None))
            else:
                self.p2hand.append(None)
            i = i + 1
        # Player1盤面情報
        # Player2盤面情報
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
        while(i < 10):
            if(i < len(p1hands)):
                self.p1hand.append(p1hands[i])
            else:
                self.p1hand.append(None)
            i = i + 1
