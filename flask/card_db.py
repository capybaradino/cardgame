import sqlite3


def getfileinfos_fromsid(sid):
    uid = getuid_fromsid(sid)
    con = sqlite3.connect('material.db')
    cur = con.cursor()
    cur.execute("select * from material where owneruid = '" + uid + "'")
    fileinfos = cur.fetchall()
    con.close()
    return fileinfos


def deletefile_fromfilename(filename, sid):
    con = sqlite3.connect('material.db')
    cur = con.cursor()
    uid = getuid_fromsid(sid)
    cur.execute("select * from material where filename = '" +
                filename + "' and owneruid = '" + uid + "'")
    if(card_fetchone(cur) is None):
        con.close()
        return False
    cur.execute("delete from material where filename = '" +
                filename + "' and owneruid = '" + uid + "'")
    con.commit()
    con.close()
    return True


def postfile(fid, owneruid, kind, original_filename, filename, upload_date):
    con = sqlite3.connect('material.db')
    cur = con.cursor()
    cur.execute("insert into material values ('" + fid + "','" +
                owneruid + "','" + kind + "','" + original_filename + "','" +
                filename + "','" + upload_date + "')")
    con.commit()
    con.close()
    return


def isexist_filename(filename):
    con = sqlite3.connect('material.db')
    cur = con.cursor()
    cur.execute(
        "select filename from material where filename = '" + filename + "'")
    if(card_fetchone(cur) is None):
        con.close()
        return False
    else:
        con.close()
        return True


def isexist_fid(fid):
    con = sqlite3.connect('material.db')
    cur = con.cursor()
    cur.execute("select filename from material where fid = '" + fid + "'")
    if(card_fetchone(cur) is None):
        con.close()
        return False
    else:
        con.close()
        return True


def card_fetchone(cur):
    item = cur.fetchone()
    if(item is not None):
        item = item[0]
    return item


def getuser_fromsid(sid):
    uid = getuid_fromsid(sid)
    user = getuser_fromuid(uid)
    return user


def getuid_fromsid(sid):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("select uid from usersession where sid = '" + sid + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid


def getuser_fromuid(uid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select * from user where uid = '" + uid + "'")
    user = card_fetchone(cur)
    con.close()
    return user


def getnickname_fromsid(sid):
    uid = getuid_fromsid(sid)
    nickname = getnickname_fromuid(uid)
    return nickname


def getnickname_fromuid(uid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select nickname from user where uid = '" + uid + "'")
    nickname = card_fetchone(cur)
    con.close()
    return nickname


def getemail_fromsid(sid):
    uid = getuid_fromsid(sid)
    email = getemail_fromuid(uid)
    return email


def getemail_fromuid(uid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select email from user where uid = '" + uid + "'")
    email = card_fetchone(cur)
    con.close()
    return email


def getsid_fromuid(uid):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("select sid from usersession where uid = '" + uid + "'")
    sid = card_fetchone(cur)
    con.close()
    return sid


def getsid_fromsid(sid):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("select sid from usersession where sid = '" + sid + "'")
    sid = card_fetchone(cur)
    con.close()
    return sid


def postusersession(sid, uid, datestr):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("insert into usersession values ('" +
                sid + "','" + uid + "','" + datestr + "')")
    con.commit()
    con.close()
    return


def putusersession(sid, datestr):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("update usersession set accessdate = '" +
                datestr + "' where sid = '" + sid + "'")
    con.commit()
    con.close()
    return


def getnickname_fromemail(email):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select nickname from user where email = '" +
                email + "'")
    username = card_fetchone(cur)
    con.close()
    return username


def getuid_fromuid(uid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select uid from user where uid = '" + uid + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid


def getnickname_fromnickname(username):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select nickname from user where nickname = '" + username + "'")
    username = card_fetchone(cur)
    con.close()
    return username


def postuser(uid, email, username):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("insert into user values ('" + uid +
                "','" + email + "','" + username + "')")
    con.commit()
    con.close()
    return


def getuid_fromemail(email):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select uid from user where email is '" + email + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid
