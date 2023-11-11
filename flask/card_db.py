import sqlite3
import uuid


# utility
def card_fetchone(cur):
    item = cur.fetchone()
    if item is not None:
        item = item[0]
    return item


def card_getcolumnno(db_name, table_name, column_name):
    # SQLite3データベースに接続
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # PRAGMAステートメントを使用してテーブルの情報を取得
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()

    # 列の情報を調べて、指定した列名の列が何列目かを取得
    column_index = None
    for column_info in columns_info:
        if column_info[1] == column_name:
            column_index = column_info[0]  # 列の位置（1から始まる）を取得
            break

    # データベース接続を閉じる
    conn.close()
    return column_index


# accesser
def isexist_gsid(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select gsid from gamesession where gsid = '" + gsid + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def isexist_player_tid(name):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select player_tid from playerstats where player_tid = '" + name + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def is_table_exists(table_name):
    db_name = "session.db"
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # sqlite_masterテーブルをクエリして指定したテーブル名が存在するか確認する
        query = (
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        )
        cursor.execute(query)

        table_exists = len(cursor.fetchall()) > 0

        conn.close()
        return table_exists
    except Exception as e:
        print(f"テーブルの存在確認中にエラーが発生しました: {e}")
        return False


def getallcids():
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select cid from card_basicdata")
    cids = cur.fetchall()
    con.close()
    return cids


def getcids_fromdeck(deck_name):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    query = f"""
        SELECT cid FROM {deck_name}
    """
    cur.execute(query)
    cids = cur.fetchall()
    con.close()
    return cids


def deletegamesession(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("delete from gamesession where gsid = '" + gsid + "'")
    con.commit()
    con.close()
    return


def getgamesession(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select * from gamesession where gsid = '" + gsid + "'")
    gamesession = cur.fetchall()
    if len(gamesession) != 0:
        gamesession = gamesession[0]
    else:
        gamesession = None
    con.close()
    return gamesession


def putsession(table_name, key_name, key, column, value):
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = f"UPDATE {table_name} SET {column} = ? WHERE {key_name} = ?"
    cursor.execute(query, (value, key))
    con.commit()
    con.close()
    return


def appendlog(card_table, value):
    con = sqlite3.connect("session.db")
    table_name = "gamesession"
    cursor = con.cursor()
    query = f"SELECT log FROM {table_name} WHERE card_table = ?"
    cursor.execute(query, (card_table,))
    text = card_fetchone(cursor)
    text = text + "," + value
    query = f"UPDATE {table_name} SET log = ? WHERE card_table = ?"
    cursor.execute(query, (text, card_table))
    con.commit()
    con.close()
    return


def appendsession(table_name, key_name, key, column, value):
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = f"SELECT {column} FROM {table_name} WHERE {key_name} = ?"
    cursor.execute(query, (key,))
    text = card_fetchone(cursor)
    text = text + "," + value
    query = f"UPDATE {table_name} SET {column} = ? WHERE {key_name} = ?"
    cursor.execute(query, (text, key))
    con.commit()
    con.close()
    return


def putgamesession(gsid, column, value):
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = f"UPDATE gamesession SET {column} = ? WHERE gsid = ?"
    cursor.execute(query, (value, gsid))
    con.commit()
    con.close()
    return


def getgsid_fromsid(sid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select gsid from usersession where sid = '" + sid + "'")
    gsid = card_fetchone(cur)
    con.close()
    return gsid


def getsid_fromgsid(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select sid from usersession where gsid = '" + gsid + "'")
    gsid = card_fetchone(cur)
    con.close()
    return gsid


def postgamesession(
    gsid, p1_player_table, p2_player_table, card_table, log, state, lastupdate
):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute(
        "insert into gamesession values (?,?,?,?,?,?,?)",
        (gsid, p1_player_table, p2_player_table, card_table, log, state, lastupdate),
    )
    con.commit()
    con.close()
    return


def postplayerstats(player_tid, name, job, hp, mp, maxmp, tension):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute(
        "insert into playerstats values (?,?,?,?,?,?,?)",
        (player_tid, name, job, hp, mp, maxmp, tension),
    )
    con.commit()
    con.close()
    return


def getplayerstats(player_tid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select * from playerstats where player_tid = '" + player_tid + "'")
    session = cur.fetchall()
    if len(session) != 0:
        session = session[0]
    else:
        session = None
    con.close()
    return session


def deleteplayerstats(player_tid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("delete from playerstats where player_tid = '" + player_tid + "'")
    con.commit()
    con.close()
    return


def createdecktable(table_name):
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # テーブルの作成
    query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            cid TEXT NOT NULL,
            loc TEXT,
            cuid PRIMARY KEY,
            locnum INTEGER,
            dhp INTEGER NOT NULL,
            dattack INTEGER NOT NULL,
            active INTEGER NOT NULL,
            turnend_effect TEXT,
            turnend_effect_ontime TEXT,
            status TEXT,
            cardname TEXT,
            rsv5 TEXT,
            rsv6 TEXT,
            rsv7 TEXT,
            rsv8 TEXT
        )
    """
    cursor.execute(query)

    conn.commit()
    conn.close()
    return


def deletedecktable(table_name):
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # テーブルの作成
    query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(query)

    conn.commit()
    conn.close()
    return


def postdeck(table_name, cid, loc):
    cardname = getcardname_fromcid(cid)
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    while True:
        # gsid生成
        cuid = str(uuid.uuid4())
        if isexist_cuid(table_name, cuid):
            continue
        break
    query = f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    cursor.execute(
        query, (cid, loc, cuid, -1, 0, 0, 0, "", "", "", cardname, "", "", "", "")
    )
    con.commit()
    con.close()
    return cuid


def putdeck(table_name, cuid, loc):
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = f"UPDATE {table_name} SET loc = ? WHERE cuid = ?"
    cursor.execute(query, (loc, cuid))
    con.commit()
    con.close()
    return


def putdeck_locnum(table_name, cuid, loc):
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = f"UPDATE {table_name} SET locnum = ? WHERE cuid = ?"
    cursor.execute(query, (loc, cuid))
    con.commit()
    con.close()
    return


def isexist_cuid(table_name, cuid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select cuid from '" + table_name + "' where cid = '" + cuid + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def getfirstcuid_fromdeck(table_name, name):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select cuid from " + table_name + " where loc = '" + name + "'")
    cuid = card_fetchone(cur)
    con.close()
    return cuid


def getcards_fromdeck(table_name, name):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select * from " + table_name + " where loc = '" + name + "'")
    cards = cur.fetchall()
    con.close()
    return cards


def getrecords_fromsession(table_name, key_name, key):
    # データベースに接続
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = f"SELECT * FROM {table_name} WHERE {key_name} = ?"
    cursor.execute(query, (key,))

    # レコードを取得
    records = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    return records


def getrecords_fromsession2(table_name, key_name, key, key_name2, key2):
    # データベースに接続
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = f"SELECT * FROM {table_name} WHERE {key_name} = ? AND {key_name2} = ?"
    cursor.execute(query, (key, key2))

    # レコードを取得
    records = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    return records


def getrecord_fromsession(table_name, key_name, key):
    # データベースに接続
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = f"SELECT * FROM {table_name} WHERE {key_name} = ?"
    cursor.execute(query, (key,))

    # レコードを取得
    record = cursor.fetchone()

    # 接続を閉じる
    conn.close()

    return record


def getrecord_fromgame(table_name, key_name, key):
    # データベースに接続
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = f"SELECT * FROM {table_name} WHERE {key_name} = ?"
    cursor.execute(query, (key,))

    # レコードを取得
    record = cursor.fetchone()

    # 接続を閉じる
    conn.close()

    return record


def deletecard_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("delete from card_basicdata where cid = '" + cid + "'")
    con.commit()
    con.close()
    return True


def getfilename_fromfid(fid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select filename from card_material where fid = '" + fid + "'")
    filename = card_fetchone(cur)
    con.close()
    return filename


def getfid_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select fid from card_basicdata where cid = '" + cid + "'")
    fid = card_fetchone(cur)
    con.close()
    return fid


def getfilename_fromcid(cid):
    fid = getfid_fromcid(cid)
    filename = getfilename_fromfid(fid)
    return filename


def getfilename_fromupname(name):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select filename from card_material where name = '" + name + "'")
    filename = card_fetchone(cur)
    con.close()
    return filename


def getcardname_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select cardname from card_basicdata where cid = '" + cid + "'")
    cardname = card_fetchone(cur)
    con.close()
    return cardname


def getcid_fromcardname(cardname):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select cid from card_basicdata where cardname = '" + cardname + "'")
    cardname = card_fetchone(cur)
    con.close()
    return cardname


def postcard(
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
):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute(
        "insert into card_basicdata values ('"
        + cid
        + "','"
        + fid
        + "','"
        + cardname
        + "','"
        + leader
        + "','"
        + cardpack
        + "','"
        + cost
        + "','"
        + category
        + "','"
        + rarity
        + "','"
        + type
        + "','"
        + attack
        + "','"
        + hp
        + "','"
        + effect
        + "','"
        + flavor
        + "')"
    )
    con.commit()
    con.close()
    return


def isexist_cid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select cid from card_basicdata where cid = '" + cid + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def getallfids_frommaterial():
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select fid from card_material")
    fids = cur.fetchall()
    con.close()
    return fids


def getfileinfos_fromsid(sid):
    uid = getuid_fromsid(sid)
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select * from card_material where owneruid = '" + uid + "'")
    fileinfos = cur.fetchall()
    con.close()
    return fileinfos


def deletefile_fromfilename(filename, sid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    uid = getuid_fromsid(sid)
    cur.execute(
        "select * from card_material where filename = '"
        + filename
        + "' and owneruid = '"
        + uid
        + "'"
    )
    if card_fetchone(cur) is None:
        con.close()
        return False
    cur.execute(
        "delete from card_material where filename = '"
        + filename
        + "' and owneruid = '"
        + uid
        + "'"
    )
    con.commit()
    con.close()
    return True


def deletefile_fromfilename_admin(filename):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select * from card_material where filename = '" + filename + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    cur.execute("delete from card_material where filename = '" + filename + "'")
    con.commit()
    con.close()
    return True


def postfile(fid, owneruid, kind, name, original_filename, filename, upload_date):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute(
        "insert into card_material values ('"
        + fid
        + "','"
        + owneruid
        + "','"
        + kind
        + "','"
        + name
        + "','"
        + original_filename
        + "','"
        + filename
        + "','"
        + upload_date
        + "')"
    )
    con.commit()
    con.close()
    return


def isexist_filename(filename):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute(
        "select filename from card_material where filename = '" + filename + "'"
    )
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def isexist_fid(fid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("select filename from card_material where fid = '" + fid + "'")
    if card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def getuser_fromsid(sid):
    uid = getuid_fromsid(sid)
    user = getuser_fromuid(uid)
    return user


def getuid_fromsid(sid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select uid from usersession where sid = '" + sid + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid


def getuser_fromuid(uid):
    con = sqlite3.connect("user.db")
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
    con = sqlite3.connect("user.db")
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
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select email from user where uid = '" + uid + "'")
    email = card_fetchone(cur)
    con.close()
    return email


def getsid_fromuid(uid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select sid from usersession where uid = '" + uid + "'")
    sid = card_fetchone(cur)
    con.close()
    return sid


def getsid_fromsid(sid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select sid from usersession where sid = '" + sid + "'")
    sid = card_fetchone(cur)
    con.close()
    return sid


def postusersession(sid, uid, datestr):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = f"insert into usersession values (?,?,?,?,?)"
    cur.execute(query, (sid, uid, datestr, "", getnickname_fromuid(uid)))
    con.commit()
    con.close()
    return


def putusersession(sid, datestr):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute(
        "update usersession set accessdate = '"
        + datestr
        + "' where sid = '"
        + sid
        + "'"
    )
    con.commit()
    con.close()
    return


def putusersession_gsid(sid, gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute(
        "update usersession set gsid = '" + gsid + "' where sid = '" + sid + "'"
    )
    con.commit()
    con.close()
    return


def deleteusersession(uid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = f"DELETE FROM usersession WHERE uid = ?"
    cur.execute(query, (uid,))
    con.commit()
    con.close()
    return


def getnickname_fromemail(email):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select nickname from user where email = '" + email + "'")
    username = card_fetchone(cur)
    con.close()
    return username


def getuid_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select uid from user where uid = '" + uid + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid


def getnickname_fromnickname(username):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select nickname from user where nickname = '" + username + "'")
    username = card_fetchone(cur)
    con.close()
    return username


def getgrant_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select grant from user where uid = '" + uid + "'")
    username = card_fetchone(cur)
    con.close()
    return username


def postuser(uid, email, username):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    query = f"INSERT INTO user VALUES (?,?,?,?)"
    cur.execute(query, (uid, email, username, ""))
    con.commit()
    con.close()
    return


def getuid_fromemail(email):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("select uid from user where email is '" + email + "'")
    uid = card_fetchone(cur)
    con.close()
    return uid
