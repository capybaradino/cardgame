import json
from flask import Flask
from api_play import api_play_hand
from api_attack import api_unit_attack
from api_spell import api_spell
import api_system
import api_view
import debug
from flask_restx import Resource, Api
import card_user
import card_db
import re
from class_playview import Play_view
from class_playdata import Playdata
from class_playinfo import Card_info
app = Flask(__name__)
api = Api(app)


def _getstatus(gsid, sid):
    if (gsid == "win" or gsid == "lose" or gsid == "matching"):
        return {"status": gsid}, 200
    elif (gsid == ""):
        return {"status": "-"}, 200
    else:
        playdata = Playdata(sid)
        if (playdata.stat == "matching"):
            return {"status": "matching"}, 200
        return {"status": "playing"}, 200


@api.route('/system/<sid>/<command>')
class Card_system(Resource):
    def post(self, sid, command):
        sid = card_user.card_checksession(sid)
        if (sid is None):
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if (gsid == ""):
            if (command == "newgame"):
                stat = api_system.newgame(sid)
                return {"info": stat}, 200
            else:
                return {"error": "gamesession not exist"}, 403

        if (sid is None):
            return {"error": "illegal session"}, 403
        if (command == "turnend"):
            return api_system.turnend(sid)
        elif (command == "surrender"):
            return api_system.surrender(sid)
        else:
            if (command == "newgame"):
                return {"error": "gamesession exists"}, 403
            else:
                return {"error": "illegal command"}, 403

    def get(self, sid, command):
        sid = card_user.card_checksession(sid)
        if (sid is None):
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if (command == "status"):
            return _getstatus(gsid, sid)
        elif (command == "result"):
            if (gsid == "win"):
                card_user.card_cleargame(sid)
                return {"info": "you win!"}, 200
            elif (gsid == "lose"):
                card_user.card_cleargame(sid)
                return {"info": "you lose..."}, 200
            elif (gsid == ""):
                return {"error": "gamesession not exist"}, 403
            else:
                return {"error": "gamesession exists"}, 403
        else:
            return {"error": "illegal command"}, 403


@api.route('/view/<sid>')
class Card_view(Resource):
    def get(self, sid):
        sid = card_user.card_checksession(sid)
        if (sid is None):
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if (gsid == ""):
            return {"error": "gamesession is null"}, 403
        playview = Play_view(sid)

        # ゲームが終了処理中でないか確認
        data, statuscode = _getstatus(gsid, sid)
        if (data["status"] != "playing"):
            return {"error": "game is over"}, 403

        return api_view.get(playview)


@api.route('/play/<sid>/<card1>/<card2>')
class Card_play(Resource):
    def post(self, sid, card1, card2):
        sid = card_user.card_checksession(sid)
        if (sid is None):
            return {"error": "illegal session"}, 403
        if (card1 is None):
            return {"error": "card1 is null"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if (gsid == ""):
            return {"error": "gamesession is null"}
        playview = Play_view(sid)

        # Player1(自分のターン)か確認
        if (playview.turnstate != "p1turn"):
            return {"error": "not in your turn"}, 403

        pattern_hand = r'^hand_[0-9]$'
        pattern_leftboard = r'leftboard_[0-5]'
        if re.match(pattern_hand, card1):
            # カードの種別を確認
            pattern = r'[0-9]'
            number = int(re.findall(pattern, card1)[0])
            hands = playview.p1hand
            objcard1: Card_info
            objcard1 = hands[number]
            if (objcard1 is None):
                return {"error": "illegal card1 number"}, 403
            if (objcard1.category == "unit"):
                # ハンドからカードをプレイ
                return api_play_hand(playview, card1, card2)
            elif (objcard1.category == "spell"):
                return api_spell(sid, playview, card1, card2)
            else:
                return {"error": "illegal card1 category"}, 403
        elif re.match(pattern_leftboard, card1):
            # ユニットで攻撃
            return api_unit_attack(sid, playview, card1, card2)
        else:
            return {"error": "illegal card1"}, 403


# Omajinai
if __name__ == "__main__":
    # 自動リロードでエラーが出る場合はVSCodeのBREAKPOINTSの"Uncaught Exceptions"のチェックを外すこと
    app.run(debug=True, port=5001)
