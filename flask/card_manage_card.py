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
        fid = request.form['fid']
        cardname = request.form['cardname']
        attack = request.form['attack']
        defense = request.form['defense']
        type1 = request.form['type1']
        type2 = request.form['type2']
        rarity = request.form['rarity']
        while True:
            cid = str(uuid.uuid4())
            if(card_db.isexist_cid(cid)):
                continue
            break
        card_db.postcard(cid, fid, cardname, attack,
                         defense, type1, type2, rarity)
        break
    return redirect(callback)


def card_management_view():
    cardinfo = card_util.card_gettablehtml_admin('card_basicdata')
    uploadedinfo = card_util.card_gettablehtml('material', None)

    # make form
    cardupdateform = ""
    cardupdateform += '<form action=card method=post enctype=multipart/form-data>'
    cardupdateform += '<table border="1">'
    columns = ("cid", "fid", "cardname", "attack",
               "defense", "type1", "type2", "rarity")
    cardupdateform += "<tr>"
    for columnname in columns:
        cardupdateform += "<td>"+columnname+"</td>"
    cardupdateform += "</tr>"
    cardupdateform += "<tr>"
    # cid
    cardupdateform += "<td>Auto</td>"
    # fid
    fids = card_db.getallfids_frommaterial()
    cardupdateform += "<td><select name=fid>"
    for fid in fids:
        value = fid[0]
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # cardname
    cardupdateform += '<td><input type="text" maxlength="32" name=cardname></td>'
    # attack
    cardupdateform += "<td><select name=attack>"
    attackvalues = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    for value in attackvalues:
        value = str(value)
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # defense
    cardupdateform += "<td><select name=defense>"
    defensevalues = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    for value in defensevalues:
        value = str(value)
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # type1
    typevalues = ("fire", "water", "wind", "dark")
    cardupdateform += "<td><select name=type1>"
    for value in typevalues:
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # type2
    cardupdateform += "<td><select name=type2>"
    for value in typevalues:
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # rarity
    cardupdateform += "<td><select name=rarity>"
    rarityvalues = ("SR", "C", "R", "SR", "SSR")
    for value in rarityvalues:
        value = str(value)
        cardupdateform += "<option value="+value+">"+value+"</option>"
    cardupdateform += "</select></td>"
    # end form
    cardupdateform += "</tr></table>"
    cardupdateform += "<input type=submit value=Register>"
    cardupdateform += "</form>"

    return render_template('manage_card.html', title='manage_card', cardinfo=cardinfo,
                           uploadedinfo=uploadedinfo, cardupdateform=cardupdateform)
