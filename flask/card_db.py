import sqlite3


def getsid_fromuid(uid):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("select sid from usersession where uid = '" + uid + "'")
    sid = cur.fetchone()[0]
    con.close()
    return sid


def getsid_fromsid(sid):
    con = sqlite3.connect('session.db')
    cur = con.cursor()
    cur.execute("select sid from usersession where sid = '" + sid + "'")
    sid = cur.fetchone()
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
    username = cur.fetchone()[0]
    con.close()
    return username


def getuid_fromuid(uid):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select uid from user where uid = '" + uid + "'")
    uid = cur.fetchone()[0]
    con.close()
    return uid


def getnickname_fromnickname(username):
    con = sqlite3.connect('user.db')
    cur = con.cursor()
    cur.execute("select nickname from user where nickname = '" + username + "'")
    username = cur.fetchone()[0]
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
    uid = cur.fetchone()[0]
    con.close()
    return uid
