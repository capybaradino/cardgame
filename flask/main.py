import card_admin
import card_play
import card_user
import card_util
import debug

from flask import (
    Flask,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.helpers import send_from_directory

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = card_admin.UPLOAD_FOLDER


@app.route("/play2/<param>", methods=["GET"])
def play2(param=None):
    sid = request.cookies.get("card_sid", None)
    sid = card_user.card_checksession(sid)
    if sid is None:
        return abort(401)
    email = request.cookies.get("card-email")
    sid = card_user.card_getsession(sid, email)
    if sid is None:
        return redirect(url_for("index"))
    else:
        return card_play.card_play_get2(sid, param)


@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")


@app.route("/<debugp>")
def debugp(debugp=None):
    if debugp == "p1":
        email = debug.getdebugparam("email1")
        if email is None:
            abort(404)
            return
        return index(email)
    elif debugp == "p2":
        email = debug.getdebugparam("email2")
        if email is None:
            abort(404)
            return
        return index(email)
    else:
        abort(404)


@app.route("/")
def index(email=None):
    if email is None:
        email = request.headers.get("X-Forwarded-Email")
    if email is None:
        abort(401)

    greetings, uid, username = card_user.card_auth(email)
    #    cookie  table   work
    # 1.  No      ANY     postsession
    # 2.  Yes     No      postsession(cookie override)
    # 3.  Yes     Yes     do nothing
    sid = request.cookies.get("card_sid", None)
    if sid is None:
        # 1.
        sid = card_user.card_postsession(uid)
    else:
        sid_chk = card_user.card_getsession(sid, email)
        if sid_chk is None:
            # 2.
            sid = card_user.card_postsession(uid)
        else:
            # 3.
            card_user.card_putsession(sid, uid)

    grant = card_user.card_getgrant(uid)
    # TODO 管理者画面
    # if grant == "admin":
    #     resp = make_response(
    #         render_template("index.html", title="Cardgame(admin)", greetings=greetings)
    #     )
    # else:
    playertablehtml = card_util.card_getwaitingsessionhtml(username)
    resp = make_response(
        render_template(
            "index2.html",
            title="Cardgame",
            greetings=greetings,
            playertablehtml=playertablehtml,
        )
    )

    resp.set_cookie("card_sid", sid)
    resp.set_cookie("card-email", email)
    card_user.card_cleargame(sid)
    return resp


@app.route("/play/<target>", methods=["GET", "POST", "DELETE"])
def play(target=None):
    sid = request.cookies.get("card_sid", None)
    sid = card_user.card_checksession(sid)
    if sid is None:
        return abort(401)
    email = request.cookies.get("card-email")
    sid = card_user.card_getsession(sid, email)
    if sid is None:
        return redirect(url_for("index"))
    if request.method == "POST":
        return card_play.card_play_post(sid, target, "card")
    if request.method == "DELETE" and target != "card":
        return card_play.card_play_delete(sid, target, "card")
    else:
        return card_play.card_play_get(sid)


@app.route("/uploads/<filename>")
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/uploads/<uploads_sub>/<filename>")
# ファイルを表示する
def uploaded_file_sub(uploads_sub, filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"], uploads_sub + "/" + filename
    )


@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", title="flask test", name=name)


# Omajinai
if __name__ == "__main__":
    # 自動リロードでエラーが出る場合はVSCodeのBREAKPOINTSの"Uncaught Exceptions"のチェックを外すこと
    app.run(debug=True)
