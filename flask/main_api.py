from flask import Flask
from api_play import api_play_hand
import debug
from flask_restx import Resource, Api
import card_user, card_db
import re
from class_playview import Play_view
from class_playinfo import Card_info
app = Flask(__name__)
api = Api(app)


@api.route('/test')
# @api.route('/play/<sid>/<card1>/<card2>')
class Test(Resource):
    def get(self):
        return {"message":"OK GET"}
    def post(self, sid, card1, card2):
        return {"message":"OK POST"}


@api.route('/play/<sid>/<card1>/<card2>')
class Card_play(Resource):
    def post(self, sid, card1, card2):
        sid = card_user.card_checksession(sid)
        if(sid is None):
            return 403
        if(card1 is None):
            return {"error": "card1 is null"}

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if(gsid == ""):
            return {"error": "gamesession is null"}
        playview = Play_view(sid)

        # Player1(自分のターン)か確認
        if(playview.turnstate != "p1turn"):
            return 401

        pattern_hand = r'^hand_[0-9]$'
        if re.match(pattern_hand, card1):
            # ハンドからカードをプレイ
            return api_play_hand(playview, card1, card2)
        else:
            return {"error": "illegal card1"}
            

        return {
            "sid": sid
        }


# Omajinai
if __name__ == "__main__":
    # 自動リロードでエラーが出る場合はVSCodeのBREAKPOINTSの"Uncaught Exceptions"のチェックを外すこと
    app.run(debug=True, port=5001)
