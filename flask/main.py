from flask import Flask, render_template
from flask import request, make_response, redirect, url_for
from flask.helpers import send_from_directory
import sqlite3
import card_user
import card_admin
import card_util
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = card_admin.UPLOAD_FOLDER


@app.route('/')
def index():
    email = request.headers.get("X-Forwarded-Email")
    greetings, uid = card_user.card_auth(email)
    #    cookie  table   work
    # 1.  No      ANY     postsession
    # 2.  Yes     No      postsession(cookie override)
    # 3.  Yes     Yes     do nothing
    sid = request.cookies.get("card_sid", None)
    if(sid is None):
        # 1.
        sid = card_user.card_postsession(uid)
    else:
        sid_chk = card_user.card_getsession(sid, email)
        if(sid_chk is None):
            # 2.
            sid = card_user.card_postsession(uid)
        else:
            # 3.
            card_user.card_putsession(sid, uid)
    resp = make_response(render_template(
        'index.html', title='Cardgame', greetings=greetings))
    resp.set_cookie("card_sid", sid)
    return resp


@app.route('/admin/<option>', methods=['GET', 'POST', 'DELETE'])
def admin(option=None):
    sid = request.cookies.get("card_sid", None)
    email = request.headers.get("X-Forwarded-Email")
    sid = card_user.card_getsession(sid, email)
    if(sid is None):
        return redirect(url_for("index"))
    if(request.method == 'POST'):
        return card_admin.card_admin_post(sid, option, request, request.url)
    if(request.method == 'DELETE' and option != "view"):
        return card_admin.card_admin_delete(sid, option, 'admin/view')
    else:
        if(option == "view"):
            return card_admin.card_admin_view(sid)
        return card_admin.card_admin_view(sid)


@app.route('/uploads/<filename>')
# ファイルを表示する
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/chkheaders/')
def chkheaders():
    headers = "<table border=1>"
    for header in request.headers:
        headers += "<tr>"
        headers += "<td>" + header[0] + "</td><td>" + header[1] + "</td>"
        headers += "</tr>"
        # envs += request.headers.get("Host")
    headers += "</table>"
    return render_template('chkheaders.html', title='Check Headers', headers=headers)


@app.route('/chktable/<tablename>')
def chkusers(tablename=None):
    headers = card_util.card_gettablehtml(tablename, None)
    return render_template('chkheaders.html', title=tablename, headers=headers)


@app.route('/management/<target>', methods=['GET', 'POST', 'DELETE'])
def management(target=None):
    sid = request.cookies.get("card_sid", None)
    email = request.headers.get("X-Forwarded-Email")
    sid = card_user.card_getsession(sid, email)
    if(sid is None):
        return redirect(url_for("index"))
#    if(request.method == 'POST'):
#        return card_admin.card_admin_post(sid, option, request, request.url)
#    if(request.method == 'DELETE' and option != "view"):
#        return card_admin.card_admin_delete(sid, option, 'management/' + target)
    else:
        cardinfo = card_util.card_gettablehtml('card_basicdata', None)
        uploadedinfo = card_util.card_gettablehtml('material', None)
        return render_template('management.html', title='management', cardinfo=cardinfo, uploadedinfo=uploadedinfo)


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', title='flask test', name=name)


# Omajinai
if __name__ == "__main__":
    app.run(debug=True)
