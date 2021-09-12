import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect
import card_db
import card_util
import uuid

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def card_admin_post(sid, option, request: request, callback):
    while True:
        if(option != "card"):
            break
        if ('file' not in request.files):
            break
        file = request.files['file']
        if file.filename == '':
            break
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            extention = file.filename.rsplit('.', 1)[1].lower()
            while True:
                filename = str(uuid.uuid4())
                filename = filename + '.' + extention
                if(card_db.isexist_filename(filename)):
                    continue
                break
            while True:
                fid = str(uuid.uuid4())
                if(card_db.isexist_fid(fid)):
                    continue
                break
            uid = card_db.getuid_fromsid(sid)
            card_db.postfile(fid, uid, option, original_filename,
                             filename, card_util.card_getdatestrnow())
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            break

    return redirect(callback)


def card_admin_view(sid):
    userinfo = "<table border=1>"
    userinfo += "<tr>"
    userinfo += "<td>" + "Mail Address" + "</td><td>" + \
        card_db.getemail_fromsid(sid) + "</td>"
    userinfo += "</tr>"
    userinfo += "<tr>"
    userinfo += "<td>" + "Nickname" + "</td><td>" + \
        card_db.getnickname_fromsid(sid) + "</td>"
    userinfo += "</tr>"
    userinfo += "</table>"
    return render_template('admin.html', title='Admin', userinfo=userinfo)
