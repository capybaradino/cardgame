from flask import Flask
import debug
from flask_restx import Resource, Api
app = Flask(__name__)
api = Api(app)


@api.route('/api/<sid>/game')
class Game(Resource):
    def get(self, sid):
        return {
            "sid": sid
        }


# Omajinai
if __name__ == "__main__":
    # 自動リロードでエラーが出る場合はVSCodeのBREAKPOINTSの"Uncaught Exceptions"のチェックを外すこと
    app.run(debug=True, port=5001)
