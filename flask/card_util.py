from datetime import datetime
import sqlite3
import card_db


def card_gettablehtml(tablename, sid):
    return card_gettablehtml_impl(tablename, sid, 'false')


def card_gettablehtml_admin(tablename):
    return card_gettablehtml_impl(tablename, None, 'true')


def card_gettablehtml_impl(tablename, sid, isadmin):
    headers = ""
    if("session" in tablename):
        con = sqlite3.connect('session.db')
    elif("card_" in tablename):
        con = sqlite3.connect('game.db')
    else:
        con = sqlite3.connect(tablename + '.db')

    cur = con.cursor()

    headers += "<table border=1>"
    headers += "<tr>"
    # 左端に画像を表示する為に1列追加
    if(tablename == 'material' or tablename == 'card_basicdata'):
        headers += "<td></td>"

    index = 0
    index_filename = 0
    index_fid = 0
    index_cid = 0
    admin_uploadtarget = (2, 3, 4, 6)
    for row in cur.execute("PRAGMA table_info('" + tablename + "')").fetchall():
        if(tablename == 'material'):
            if (row[1] == "filename"):
                index_filename = index
            if(sid is not None):
                if(index not in admin_uploadtarget):
                    index += 1
                    continue
        if(tablename == 'card_basicdata'):
            if (row[1] == "fid"):
                index_fid = index
            if (row[1] == "cid"):
                index_cid = index
        headers += "<td>"
        headers += str(row[1]) + " (" + str(row[2]) + ")"
        headers += "</td>"
        index += 1
    if(isadmin == 'true'):
        headers += "<td></td>"
    headers += "</tr>\n"

    if(sid is None):
        rows = cur.execute('select * from ' + tablename)
    else:
        rows = card_db.getfileinfos_fromsid(sid)

    for row in rows:
        headers += "<tr>"
        filename = None
        if(tablename == 'material'):
            filename = row[index_filename]
        if(tablename == 'card_basicdata'):
            fid = row[index_fid]
            filename = card_db.getfilename_fromfid(fid)
        if filename:
            headers += "<td>" + "<img width=100 src=\"" + \
                "../uploads/" + filename + "\"></td>"
        index = 0
        for item in row:
            if(sid is not None):
                if(index not in admin_uploadtarget):
                    index += 1
                    continue
            headers += "<td>" + str(item) + "</td>"
            index += 1
        if(sid is not None and tablename == 'material'):
            headers += "<td>" + \
                "<input type=button value=Delete onclick=\"send_delete(\'" + \
                filename + "\');\"/>" + \
                "</td>"
        if(tablename == 'material' and isadmin == 'true'):
            headers += "<td>" + \
                "<input type=button value=Delete onclick=\"send_delete(\'" + \
                filename + "\');\"/>" + \
                "</td>"
        if(tablename == 'card_basicdata' and isadmin == 'true'):
            cid = row[index_cid]
            headers += "<td>" + \
                "<input type=button value=Delete onclick=\"send_delete(\'" + \
                cid + "\');\"/>" + \
                "</td>"
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
