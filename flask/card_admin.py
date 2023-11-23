import os
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect
import card_db
import card_util
import uuid
import card_image

UPLOAD_FOLDER = "./uploads"
TMP_FOLDEF = "/tmp"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in card_image.ALLOWED_EXTENSIONS
    )


def check_file(sid, file):
    tmpfile = os.path.join(TMP_FOLDEF, "card_" + sid)
    file.save(tmpfile)
    ret = card_image.checksize(tmpfile)
    if ret == False:
        os.remove(tmpfile)
    return ret, tmpfile


def card_admin_delete(sid, option, callback):
    while True:
        if not card_db.deletefile_fromfilename(option, sid):
            break
        os.remove(os.path.join(UPLOAD_FOLDER, option))
    return redirect(callback)


def card_admin_post(sid, option, request: request, callback):
    while True:
        if option != "card":
            break
        if "file" not in request.files:
            break
        file = request.files["file"]
        if file.filename == "":
            break
        name = request.form["name"]
        if name is None:
            break
        if file:
            chkallowed = allowed_file(file.filename)
            chkfile, tmpfile = check_file(sid, file)
        if chkallowed and chkfile:
            original_filename = secure_filename(file.filename)
            extention = file.filename.rsplit(".", 1)[1].lower()
            while True:
                filename = str(uuid.uuid4())
                filename = filename + "." + extention
                if card_db.isexist_filename(filename):
                    continue
                break
            while True:
                fid = str(uuid.uuid4())
                if card_db.isexist_fid(fid):
                    continue
                break
            uid = card_db.getuid_fromsid(sid)
            card_db.postfile(
                fid,
                uid,
                option,
                name,
                original_filename,
                filename,
                card_util.card_getdatestrnow(),
            )
            os.replace(tmpfile, os.path.join(UPLOAD_FOLDER, filename))
            break
        else:
            break
    return redirect(callback)


def card_admin_view(sid):
    userinfo = "<table border=1>"
    userinfo += "<tr>"
    userinfo += (
        "<td>" + "Mail Address" + "</td><td>" + card_db.getemail_fromsid(sid) + "</td>"
    )
    userinfo += "</tr>"
    userinfo += "<tr>"
    userinfo += (
        "<td>" + "Nickname" + "</td><td>" + card_db.getnickname_fromsid(sid) + "</td>"
    )
    userinfo += "</tr>"
    userinfo += "</table>"

    upinfo = card_util.card_gettablehtml("card_material", sid)

    return render_template(
        "admin.html", title="Admin", userinfo=userinfo, upinfo=upinfo
    )
