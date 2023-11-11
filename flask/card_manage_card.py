import uuid
from flask import render_template
from flask.globals import request
from werkzeug.utils import redirect
import card_util
import card_db


def card_management_delete(cid, callback):
    card_db.deletecard_fromcid(cid)
    return redirect(callback)


def card_management_post(request: request, callback):
    while True:
        fid = request.form["fid"]
        cardname = request.form["cardname"]
        leader = request.form["leader"]
        cardpack = request.form["cardpack"]
        cost = request.form["cost"]
        category = request.form["category"]
        rarity = request.form["rarity"]
        type = request.form["type"]
        attack = request.form["attack"]
        hp = request.form["hp"]
        effect = request.form["effect"]
        flavor = request.form["flavor"]
        while True:
            cid = str(uuid.uuid4())
            if card_db.isexist_cid(cid):
                continue
            break
        card_db.postcard(
            cid,
            fid,
            cardname,
            leader,
            cardpack,
            cost,
            category,
            rarity,
            type,
            attack,
            hp,
            effect,
            flavor,
        )
        break
    return redirect(callback)


def selectform(name, cardupdateform, values):
    cardupdateform += "<td><select name=" + name + ">"
    for value in values:
        value = str(value)
        cardupdateform += "<option value=" + value + ">" + value + "</option>"
    cardupdateform += "</select></td>"
    return cardupdateform


def card_management_view():
    cardinfo = card_util.card_gettablehtml_admin("card_basicdata")
    uploadedinfo = card_util.card_gettablehtml("card_material", None)

    # make form
    cardupdateform = ""
    cardupdateform += "<form action=card method=post enctype=multipart/form-data>"
    cardupdateform += '<table border="1">'
    columns = (
        "cid",
        "fid",
        "cardname",
        "leader",
        "cardpack",
        "cost",
        "category",
        "rarity",
        "type",
        "attack",
        "hp",
        "effect",
        "flavor",
    )
    cardupdateform += "<tr>"
    for columnname in columns:
        cardupdateform += "<td>" + columnname + "</td>"
    cardupdateform += "</tr>"
    cardupdateform += "<tr>"
    # cid
    cardupdateform += "<td>Auto</td>"
    # fid
    fids = card_db.getallfids_frommaterial()
    cardupdateform += "<td><select name=fid>"
    for fid in fids:
        value = fid[0]
        cardupdateform += "<option value=" + value + ">" + value + "</option>"
    cardupdateform += "</select></td>"
    # cardname
    cardupdateform += '<td><input type="text" maxlength="32" name=cardname></td>'
    # leader
    name = "leader"
    values = ("common", "kensi")
    cardupdateform = selectform(name, cardupdateform, values)
    # leader
    name = "cardpack"
    values = ("basic", "standard")
    cardupdateform = selectform(name, cardupdateform, values)
    # cost
    name = "cost"
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    cardupdateform = selectform(name, cardupdateform, values)
    # category
    name = "category"
    values = ("unit", "skill")
    cardupdateform = selectform(name, cardupdateform, values)
    # rarity
    name = "rarity"
    values = ("normal", "rare", "super", "legend")
    cardupdateform = selectform(name, cardupdateform, values)
    # type
    name = "type"
    values = ("", "slime")
    cardupdateform = selectform(name, cardupdateform, values)
    # attack
    name = "attack"
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    cardupdateform = selectform(name, cardupdateform, values)
    # hp
    name = "hp"
    values = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    cardupdateform = selectform(name, cardupdateform, values)
    # effect
    cardupdateform += '<td><input type="text" maxlength="32" name=effect></td>'
    # flavor
    cardupdateform += '<td><input type="text" maxlength="32" name=flavor></td>'
    # end form
    cardupdateform += "</tr></table>"
    cardupdateform += "<input type=submit value=Register>"
    cardupdateform += "</form>"

    return render_template(
        "manage_card.html",
        title="manage_card",
        cardinfo=cardinfo,
        uploadedinfo=uploadedinfo,
        cardupdateform=cardupdateform,
    )
