import json
import re

import api_system
import api_view
import card_db
import card_user
import debug
from api_attack import api_unit_attack
from api_play import api_play_hand
from api_spell import api_spell
from api_tension import api_tension
from class_playdata import Playdata
from class_playinfo import Card_info
from class_playview import Play_view
from flask_restx import Api, Resource, fields

from flask import Flask

app = Flask(__name__)
api = Api(app)


def _getstatus(gsid, sid):
    if gsid == "win" or gsid == "lose" or gsid == "matching":
        return {"status": gsid}, 200
    elif gsid == "":
        return {"status": "-"}, 200
    else:
        playdata = Playdata(sid)
        if playdata.stat == "matching":
            return {"status": "matching"}, 200
        return {"status": "playing"}, 200

def _isUUID(gsid):
    if re.match(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
                r"[0-9a-f]{4}-[0-9a-f]{12}", gsid) is None:
        return False
    return True

@api.route("/system/<sid>/<command>")
class Card_system(Resource):
    def post(self, sid, command):
        sid = card_user.card_checksession(sid)
        if sid is None:
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if _isUUID(gsid) is False:
            if command == "newgame":
                stat = api_system.newgame(sid)
                return {"info": stat}, 200
            else:
                return {"error": "gamesession not exist"}, 403

        if sid is None:
            return {"error": "illegal session"}, 403
        if command == "turnend":
            return api_system.turnend(sid)
        elif command == "surrender":
            return api_system.surrender(sid)
        else:
            if command == "newgame":
                return {"error": "gamesession exists"}, 403
            else:
                return {"error": "illegal command"}, 403

    def get(self, sid, command):
        sid = card_user.card_checksession(sid)
        if sid is None:
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if gsid == "":
            return {"error": "gamesession and result not exist"}, 403
        if command == "status":
            return _getstatus(gsid, sid)
        elif command == "result":
            if gsid == "win":
                card_user.card_cleargame(sid)
                return {"info": "you win!"}, 200
            elif gsid == "lose":
                card_user.card_cleargame(sid)
                return {"info": "you lose..."}, 200
            elif gsid == "":
                return {"error": "gamesession not exist"}, 403
            else:
                return {"error": "gamesession exists"}, 403
        else:
            return {"error": "illegal command"}, 403


hand = api.model(
    "hand",
    dict(
        cost=fields.Integer("2"),
        attack=fields.Integer("-1"),
        attack_org=fields.Integer("-1"),
        hp=fields.Integer("-1"),
        hp_org=fields.Integer("-1"),
        name=fields.String("merami"),
        graphic=fields.String("uploads/test/merami.png"),
        category=fields.String("spell"),
        effect=fields.String("any_3dmg"),
    ),
)


board = api.model(
    "board",
    dict(
        location=fields.Integer("0"),
        active=fields.Integer("0"),
        cost=fields.Integer("2"),
        attack=fields.Integer("1"),
        attack_org=fields.Integer("1"),
        hp=fields.Integer("1"),
        hp_org=fields.Integer("1"),
        name=fields.String("magicfly"),
        graphic=fields.String("uploads/test/magicfly.png"),
        category=fields.String("unit"),
        effect=fields.String("ondead:self_1draw_spell"),
        status=fields.String(""),
    ),
)

player1 = api.model(
    "player1",
    dict(
        name=fields.String("Skoog"),
        HP=fields.Integer("9"),
        decknum=fields.Integer("24"),
        MP=fields.Integer("1"),
        maxMP=fields.Integer("3"),
        tension=fields.Integer("2"),
        tension_active=fields.Integer("1"),
        hand=fields.List(fields.Nested(hand)),
        board=fields.List(fields.Nested(board)),
    ),
)


player2 = api.model(
    "player2",
    dict(
        name=fields.String("Jenkins"),
        HP=fields.Integer("10"),
        decknum=fields.Integer("23"),
        MP=fields.Integer("3"),
        maxMP=fields.Integer("4"),
        tension=fields.Integer("1"),
        handnum=fields.Integer("3"),
        board=fields.List(fields.Nested(board)),
    ),
)

view_model = api.model(
    "view",
    dict(
        turn=fields.String("p2turn"),
        player1=fields.Nested(player1),
        player2=fields.Nested(player2),
    ),
)


@api.route("/view/<sid>")
@api.doc(params={"sid": "Session ID"})
class Card_view(Resource):
    @api.response(200, "Success", view_model)
    @api.response(403, "Forbidden (See response message)")
    def get(self, sid):
        sid = card_user.card_checksession(sid)
        if sid is None:
            return {"error": "illegal session"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if _isUUID(gsid) is False:
            return {"error": "gamesession is null"}, 403
        playview = Play_view(sid)

        # ゲームが終了処理中でないか確認
        data, statuscode = _getstatus(gsid, sid)
        if data["status"] != "playing":
            return {"error": "game is over"}, 403

        return api_view.get(playview)


@api.route("/play/<sid>/<card1>/<card2>")
@api.doc(
    params={
        "sid": "Session ID",
        "card1": "A card location name you want to play.",
        "card2": "A location where the card1 want to play to.",
    }
)
class Card_play(Resource):
    @api.doc(responses={403: "Not Authorized"})
    def post(self, sid, card1, card2):
        sid = card_user.card_checksession(sid)
        if sid is None:
            return {"error": "illegal session"}, 403
        if card1 is None:
            return {"error": "card1 is null"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        # gsidがUUIDでなければエラー
        if _isUUID(gsid) is False:
            return {"error": "gamesession is null"}
        playview = Play_view(sid)

        # Player1(自分のターン)か確認
        if playview.turnstate != "p1turn":
            return {"error": "not in your turn"}, 403

        pattern_hand = r"^hand_[0-9]$"
        pattern_leftboard = r"leftboard_[0-5]"
        pattern_tension = r"^hand_10$"
        if re.match(pattern_hand, card1):
            # カードの種別を確認
            pattern = r"[0-9]"
            number = int(re.findall(pattern, card1)[0])
            hands = playview.p1hand
            objcard1: Card_info
            objcard1 = hands[number]
            if objcard1 is None:
                return {"error": "illegal card1 number"}, 403
            if objcard1.category == "unit":
                # ハンドからカードをプレイ
                return api_play_hand(sid, playview, card1, card2, None)
            elif objcard1.category == "spell":
                return api_spell(sid, playview, card1, card2)
            else:
                return {"error": "illegal card1 category"}, 403
        elif re.match(pattern_leftboard, card1):
            # ユニットで攻撃
            return api_unit_attack(sid, playview, card1, card2)
        elif re.match(pattern_tension, card1):
            # テンションアップ
            return api_tension(sid, playview, card1, card2)
        else:
            return {"error": "illegal card1"}, 403


@api.route("/play/<sid>/<card1>/<card2>/<card3>")
class Card_play2(Resource):
    def post(self, sid, card1, card2, card3):
        sid = card_user.card_checksession(sid)
        if sid is None:
            return {"error": "illegal session"}, 403
        if card1 is None:
            return {"error": "card1 is null"}, 403
        if card2 is None:
            return {"error": "card2 is null"}, 403

        # 既存ゲームがあるか確認
        gsid = card_db.getgsid_fromsid(sid)
        if _isUUID(gsid) is False:
            return {"error": "gamesession is null"}
        playview = Play_view(sid)

        # Player1(自分のターン)か確認
        if playview.turnstate != "p1turn":
            return {"error": "not in your turn"}, 403

        pattern_hand = r"^hand_[0-9]$"
        pattern_leftboard = r"leftboard_[0-5]"
        pattern_tension = r"^hand_10$"
        if re.match(pattern_hand, card1):
            # カードの種別を確認
            pattern = r"[0-9]"
            number = int(re.findall(pattern, card1)[0])
            hands = playview.p1hand
            objcard1: Card_info
            objcard1 = hands[number]
            if objcard1 is None:
                return {"error": "illegal card1 number"}, 403
            if objcard1.category == "unit":
                # ハンドからカードをプレイ
                return api_play_hand(sid, playview, card1, card2, card3)
            elif objcard1.category == "spell":
                # TODO ３枚目対応
                return api_spell(sid, playview, card1, card2)
            else:
                return {"error": "illegal card1 category"}, 403
        elif re.match(pattern_leftboard, card1):
            # ユニットで攻撃
            # TODO ３枚目対応
            return api_unit_attack(sid, playview, card1, card2)
        elif re.match(pattern_tension, card1):
            # テンションアップ
            # TODO ３枚目対応
            return api_tension(sid, playview, card1, card2)
        else:
            return {"error": "illegal card1"}, 403


# Omajinai
if __name__ == "__main__":
    # 自動リロードでエラーが出る場合はVSCodeのBREAKPOINTSの"Uncaught Exceptions"のチェックを外すこと
    app.run(debug=True, port=5001)
