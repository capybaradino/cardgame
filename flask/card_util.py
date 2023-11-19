import sqlite3
from datetime import datetime

import card_db


def _getnamefromtid(p1_player_tid, p2_player_tid):
    p1_player_name = card_db.getrecord_fromsession(
        "playerstats", "player_tid", p1_player_tid
    )[1]
    if p2_player_tid != "waiting":
        p2_player_name = card_db.getrecord_fromsession(
            "playerstats", "player_tid", tid2
        )[1]
    else:
        p2_player_name = "waiting"
    return p1_player_name, p2_player_name


def card_getwaitingsessionhtml(username):
    # マッチング待機中のセッションを取得する
    gamesessions = card_db.getrecords_fromsession(
        "gamesession", "p2_player_tid", "waiting"
    )
    # HTMLでテーブルを作成する
    headers = ""
    headers += "<table border=1>"
    headers += "<tr>"
    headers += "<td>player1</td>"
    headers += "<td>player2</td>"
    headers += "<td>menu</td>"
    headers += "<td>option</td>"
    headers += "</tr>"
    isMatchExist = False
    for gamesession in gamesessions:
        # player1またはplayer2に自分の名前がある場合は表示
        p1_player_tid = gamesession[1]
        p2_player_tid = gamesession[2]
        p1_player_name, p2_player_name = _getnamefromtid(p1_player_tid, p2_player_tid)
        if p1_player_name == username or p2_player_name == username:
            headers += "<tr>"
            headers += "<td>" + p1_player_name + "</td>"
            headers += "<td>" + p2_player_name + "</td>"
            headers += (
                "<td>"
                + '<a href="play2/'
                + gamesession[0]
                + '">Reconnect</a>'
                + "</td>"
            )
            if p2_player_name == "waiting":
                msg = '<a href="play2/cancel">Cancel</a>'
            else:
                msg = '<a href="play2/surrender">Surrender</a>'
            headers += (
                "<td>"
                + msg
                + "</td>"
            )
            headers += "</tr>"
            isMatchExist = True

    for gamesession in gamesessions:
        gsid = gamesession[0]
        p1_player_tid = gamesession[1]
        p2_player_tid = gamesession[2]
        # player1またはplayer2に自分の名前がある場合は非表示
        p1_player_name, p2_player_name = _getnamefromtid(p1_player_tid, p2_player_tid)
        if p1_player_name == username or p2_player_name == username:
            continue
        headers += "<tr>"
        headers += "<td>" + p1_player_name + "</td>"
        headers += "<td>" + p2_player_name + "</td>"
        if isMatchExist:
            headers += "<td>" + "Join" + "</td>"
        else:
            headers += "<td>" + '<a href="play2/' + gsid + '">Join</a>' + "</td>"
        headers += "</tr>"
    headers += "</table>"
    return headers


def card_gettablehtml(tablename, sid):
    return card_gettablehtml_impl(tablename, sid, "false")


def card_gettablehtml_admin(tablename):
    return card_gettablehtml_impl(tablename, None, "true")


def card_gettablehtml_impl(tablename, sid, isadmin):
    headers = ""
    if "session" in tablename:
        con = sqlite3.connect("session.db")
    elif "card_" in tablename:
        con = sqlite3.connect("game.db")
    else:
        con = sqlite3.connect(tablename + ".db")

    cur = con.cursor()

    headers += "<table border=1>"
    headers += "<tr>"
    # 左端に画像を表示する為に1列追加
    if tablename == "card_material" or tablename == "card_basicdata":
        headers += "<td>image</td>"

    index = 0
    index_filename = 0
    index_fid = 0
    index_cid = 0
    admin_uploadtarget = (2, 3, 4, 6)
    for row in cur.execute("PRAGMA table_info('" + tablename + "')").fetchall():
        if tablename == "card_material":
            if row[1] == "filename":
                index_filename = index
            if sid is not None:
                if index not in admin_uploadtarget:
                    index += 1
                    continue
        if tablename == "card_basicdata":
            if row[1] == "fid":
                index_fid = index
            if row[1] == "cid":
                index_cid = index
        headers += "<td>"
        headers += str(row[1]) + " (" + str(row[2]) + ")"
        headers += "</td>"
        index += 1
    if isadmin == "true":
        headers += "<td></td>"
    headers += "</tr>\n"

    if sid is None:
        rows = cur.execute("select * from " + tablename)
    else:
        rows = card_db.getfileinfos_fromsid(sid)

    for row in rows:
        headers += "<tr>"
        filename = None
        if tablename == "card_material":
            filename = row[index_filename]
        if tablename == "card_basicdata":
            fid = row[index_fid]
            filename = card_db.getfilename_fromfid(fid)
        if filename:
            headers += (
                "<td>" + '<img width=100 src="' + "../uploads/" + filename + '"></td>'
            )
        index = 0
        for item in row:
            if sid is not None:
                if index not in admin_uploadtarget:
                    index += 1
                    continue
            headers += "<td>" + str(item) + "</td>"
            index += 1
        if sid is not None and tablename == "card_material":
            headers += (
                "<td>"
                + "<input type=button value=Delete onclick=\"send_delete('"
                + filename
                + "');\"/>"
                + "</td>"
            )
        if tablename == "card_material" and isadmin == "true":
            headers += (
                "<td>"
                + "<input type=button value=Delete onclick=\"send_delete('"
                + filename
                + "');\"/>"
                + "</td>"
            )
        if tablename == "card_basicdata" and isadmin == "true":
            cid = row[index_cid]
            headers += (
                "<td>"
                + "<input type=button value=Delete onclick=\"send_delete('"
                + cid
                + "');\"/>"
                + "</td>"
            )
        headers += "</tr>"
    headers += "</table>"

    con.close()
    return headers


def card_getdatestrnow():
    dt_now = datetime.now()
    return card_getdatestr(dt_now)


def card_getdatestr(dt):
    return dt.isoformat()


def card_getdatenow():
    return datetime.now()


def card_getdate(dt):
    return datetime.fromisoformat(dt)
