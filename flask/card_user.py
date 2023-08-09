import sqlite3
import names
import uuid
import card_util
import card_db


def card_checksession(sid):
    if(sid is not None):
        sid = card_db.getsid_fromsid(sid)
    return sid


def card_getsession(sid, email):
    # Check email for security
    if(sid is not None):
        sid = card_db.getsid_fromsid(sid)
        if(sid is not None):
            email_chk = card_db.getemail_fromsid(sid)
            if(email != email_chk):
                sid = None
    return sid


def card_postsession(uid):
    while True:
        sid = str(uuid.uuid4())
        sid_chk = card_db.getsid_fromsid(sid)
        if(sid_chk is not None):
            continue
        break
    datestr = card_util.card_getdatestrnow()
    card_db.postusersession(sid, uid, datestr)
    return sid


def card_putsession(sid, uid):
    nowstr = card_util.card_getdatestrnow()
    sid_chk = card_db.getsid_fromsid(sid)
    if(sid_chk is None):
        card_db.postusersession(sid, uid, nowstr)
    else:
        card_db.putusersession(sid, nowstr)
    return


def card_auth(email):
    username = None
    username = card_db.getnickname_fromemail(email)
    if(username is None):
        while True:
            uid = str(uuid.uuid4())
            uid_chk = card_db.getuid_fromuid(uid)
            if(uid_chk is not None):
                greetings = "Sorry, please reload page and try again."
                break
            username = names.get_last_name()
            username_chk = card_db.getnickname_fromnickname(username)
            if(username_chk is not None):
                greetings = "Sorry, please reload page and try again."
                break
            card_db.postuser(uid, email, username)
            greetings = "Hello, " + username + "! Your name was made randomly."
            break
    else:
        username = ''.join(username)
        uid = card_db.getuid_fromemail(email)
        greetings = "Hello, " + username + "!"

    return greetings, uid


def card_cleargame(sid):
    card_db.putusersession_gsid(sid, '')
