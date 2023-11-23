import sqlite3
import uuid


# utility
def _card_fetchone(cur):
    item = cur.fetchone()
    if item is not None:
        item = item[0]
    return item


def _isValidtable_name(table_name):
    # table_nameの先頭のc_を削除する
    table_name_forcheck = table_name[2:]
    # table_name_forcheckの_を-に置換する
    table_name_forcheck = table_name_forcheck.replace("_", "-")
    return _isValidUuid(table_name_forcheck)


def _isValidUuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise ValueError("table_name must be UUID or test_card_table")
    return True


# accessor
def isexist_gsid(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("select gsid from gamesession where gsid = ?", (gsid,))
    if _card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def isexist_player_tid(name):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT player_tid FROM playerstats WHERE player_tid = ?", (name,))
    if _card_fetchone(cur) is None:
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
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        cursor.execute(query, (table_name,))

        table_exists = len(cursor.fetchall()) > 0

        conn.close()
        return table_exists
    except Exception as e:
        print(f"An error occurred during table check: {e}")
        return False


def getcids_fromdeck(deck_name):
    # deck_nameが半角英数字と_で構成されているかどうかを判定
    if not deck_name.isalnum() and "_" not in deck_name:
        # 半角英数字と_で構成されていない場合はエラー
        raise ValueError("deck_name must be alphanumeric and _")
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    query = "SELECT cid FROM {}".format(deck_name)
    cur.execute(query)
    cids = cur.fetchall()
    con.close()
    return cids


def deletegamesession(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "DELETE FROM gamesession WHERE gsid = ?"
    cur.execute(query, (gsid,))
    con.commit()
    con.close()
    return


def getallgamesessions():
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "SELECT * FROM gamesession"
    cur.execute(query)
    gamesessions = cur.fetchall()
    con.close()
    return gamesessions


def getgamesessions(key_name, key):
    # key_nameがgsid, p1_player_tid, p2_player_tidであるかどうかを判定
    if key_name not in ["gsid", "p1_player_tid", "p2_player_tid", "card_table"]:
        # gsid, p1_player_tid, p2_player_tidでない場合はエラー
        raise ValueError("key_name must be gsid, p1_player_tid, p2_player_tid")
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "SELECT * FROM gamesession WHERE {} = ?".format(key_name)
    cur.execute(query, (key,))
    gamesessions = cur.fetchall()
    con.close()
    return gamesessions


def getgamesession(key_name, key):
    gamesessions = getgamesessions(key_name, key)
    if len(gamesessions) != 0:
        gamesession = gamesessions[0]
    else:
        gamesession = None
    return gamesession


def putplayerstats(key_name, key, column, value):
    # key_nameがplayer_tid, nameであるかどうかを判定
    if key_name not in ["player_tid", "name"]:
        # player_tid, nameでない場合はエラー
        raise ValueError("key_name must be player_tid, name")
    # columnがjob, hp, mp, maxmp, tension, skillboostであるかどうかを判定
    if column not in [
        "job",
        "hp",
        "mp",
        "maxmp",
        "tension",
        "skillboost",
    ]:
        # job, hp, mp, maxmp, tension, skillboostでない場合はエラー
        raise ValueError("column must be job, hp, mp, maxmp, tension, skillboost")
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "UPDATE playerstats SET {} = ? WHERE {} = ?".format(column, key_name)
    cursor.execute(query, (value, key))
    con.commit()
    con.close()
    return


def putcardtable(table_name, key_name, key, column, value):
    """
    カードテーブルの指定された行の指定された列の値を更新します。

    Args:
        table_name (str): テーブル名
        key_name (str): キーの列名
        key (str): キーの値
        column (str): 更新する列名
        value (str): 更新する値

    Returns:
        None
    """
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    # key_nameがcuid, loc, locnumであるかどうかを判定
    if key_name not in ["cuid", "loc", "locnum"]:
        # cuid, loc, locnumでない場合はエラー
        raise ValueError("key_name must be cuid, loc, locnum")
    # columnがloc, locnum, dhp, dattack, active, turnend_effect, turnend_effect_ontime, statusであるかどうかを判定
    if column not in [
        "loc",
        "locnum",
        "dhp",
        "dattack",
        "active",
        "turnend_effect",
        "turnend_effect_ontime",
        "status",
    ]:
        # loc, locnum, dhp, dattack, active, turnend_effect, turnend_effect_ontime, statusでない場合はエラー
        raise ValueError(
            "column must be loc, locnum, dhp, dattack, active, turnend_effect, turnend_effect_ontime, status"
        )
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "UPDATE {} SET {} = ? WHERE {} = ?".format(table_name, column, key_name)
    cursor.execute(query, (value, key))
    con.commit()
    con.close()
    return


def appendlog(card_table, value):
    """
    ゲームセッションのカードテーブルのログに値を追加します。

    Args:
        card_table (str): カードテーブルの名前。
        value (str): ログに追加する値。

    Returns:
        None
    """
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "SELECT log FROM gamesession WHERE card_table = ?"
    cursor.execute(
        query,
        (card_table,),
    )
    text = _card_fetchone(cursor)
    text = text + "," + value
    query = "UPDATE gamesession SET log = ? WHERE card_table = ?"
    cursor.execute(query, (text, card_table))
    con.commit()
    con.close()
    return


def appendsession(table_name, key_name, key, column, value):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    # key_nameがcuid, loc, locnumであるかどうかを判定
    if key_name not in ["cuid", "loc", "locnum"]:
        # cuid, loc, locnumでない場合はエラー
        raise ValueError("key_name must be cuid, loc, locnum")
    # columnがdhp, dattack, active, turnend_effect, turnend_effect_ontime, statusであるかどうかを判定
    if column not in [
        "dhp",
        "dattack",
        "active",
        "turnend_effect",
        "turnend_effect_ontime",
        "status",
    ]:
        # dhp, dattack, active, turnend_effect, turnend_effect_ontime, statusでない場合はエラー
        raise ValueError(
            "column must be dhp, dattack, active, turnend_effect, turnend_effect_ontime, status"
        )
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "SELECT {} FROM {} WHERE {} = ?".format(column, table_name, key_name)
    cursor.execute(query, (key,))
    text = _card_fetchone(cursor)
    text = text + "," + value
    query = "UPDATE {} SET {} = ? WHERE {} = ?".format(table_name, column, key_name)
    cursor.execute(query, (text, key))
    con.commit()
    con.close()
    return


def putgamesession(gsid, column, value):
    # columnがp1_player_tid, p2_player_tid, card_table, log, state, lastupdateであるかどうかを判定
    if column not in [
        "p1_player_tid",
        "p2_player_tid",
        "card_table",
        "log",
        "state",
        "lastupdate",
    ]:
        # p1_player_tid, p2_player_tid, card_table, log, state, lastupdateでない場合はエラー
        raise ValueError(
            "column must be p1_player_tid, p2_player_tid, card_table, log, state, lastupdate"
        )
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "UPDATE gamesession SET {} = ? WHERE gsid = ?".format(column)
    cursor.execute(query, (value, gsid))
    con.commit()
    con.close()
    return


def getgsid_fromsid(sid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT gsid FROM usersession WHERE sid = ?", (sid,))
    gsid = _card_fetchone(cur)
    con.close()
    return gsid


def getsid_fromgsid(gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT sid FROM usersession WHERE gsid = ?", (gsid,))
    sid = _card_fetchone(cur)
    con.close()
    return sid


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


def postplayerstats(player_tid, name, job, hp, mp, maxmp, tension, skillboost=0):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute(
        "insert into playerstats values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (
            player_tid,
            name,
            job,
            hp,
            mp,
            maxmp,
            tension,
            skillboost,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ),
    )
    con.commit()
    con.close()
    return


def getplayerstats_bytid(player_tid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM playerstats WHERE player_tid = ?", (player_tid,))
    session = cur.fetchone()
    con.close()
    return session


def getplayerstats_byname(name):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM playerstats WHERE name = ?", (name,))
    session = cur.fetchone()
    con.close()
    return session


def deleteplayerstats(player_tid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("DELETE FROM playerstats WHERE player_tid = ?", (player_tid,))
    con.commit()
    con.close()
    return


def createdecktable(table_name):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cur = con.cursor()

    # テーブルの作成
    query = """
        CREATE TABLE IF NOT EXISTS {} (
            cid TEXT NOT NULL,
            loc TEXT,
            cuid TEXT PRIMARY KEY,
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
    """.format(
        table_name
    )
    cur.execute(query)

    con.commit()
    con.close()
    return


def deletedecktable(table_name):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cur = con.cursor()

    # テーブルの削除
    query = "DROP TABLE IF EXISTS {}".format(table_name)
    cur.execute(query)

    con.commit()
    con.close()
    return


def postdeck(table_name, cid, loc):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    cardname = getcardname_fromcid(cid)
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    while True:
        # gsid生成
        cuid = str(uuid.uuid4())
        if isexist_cuid(table_name, cuid):
            continue
        break
    query = "INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)".format(table_name)
    cursor.execute(
        query,
        (cid, loc, cuid, -1, 0, 0, 0, "", "", "", cardname, "", "", "", ""),
    )
    con.commit()
    con.close()
    return cuid


def putdeck(table_name, cuid, loc):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "UPDATE {} SET loc = ? WHERE cuid = ?".format(table_name)
    cursor.execute(query, (loc, cuid))
    con.commit()
    con.close()
    return


def putdeck_locnum(table_name, cuid, loc):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cursor = con.cursor()
    query = "UPDATE {} SET locnum = ? WHERE cuid = ?".format(table_name)
    cursor.execute(query, (loc, cuid))
    con.commit()
    con.close()
    return


def isexist_cuid(table_name, cuid):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "SELECT cuid FROM {} WHERE cuid = ?".format(table_name)
    cur.execute(query, (cuid,))
    if cur.fetchone() is None:
        con.close()
        return False
    else:
        con.close()
        return True


def getfirstcuid_fromdeck(table_name, name):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "SELECT cuid FROM {} WHERE loc = ?".format(table_name)
    cur.execute(query, (name,))
    cuid = _card_fetchone(cur)
    con.close()
    return cuid


def getcards_fromdeck(table_name, name):
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "SELECT * FROM {} WHERE loc = ?".format(table_name)
    cur.execute(query, (name,))
    cards = cur.fetchall()
    con.close()
    return cards


def getrecords_fromsession(table_name, key_name, key):
    """
    データベースから指定されたテーブル名、キー名、キーに一致するレコード(複数)を取得します。

    Args:
        table_name (str): テーブル名
        key_name (str): キー名
        key (str): キー

    Returns:
        list: レコードのリスト
    """
    # table_nameのバリデーション
    _isValidtable_name(table_name)
    # key_nameがcuid, loc, locnumであるかどうかを判定
    if key_name not in ["cuid", "loc", "locnum"]:
        # cuid, loc, locnumでない場合はエラー
        raise ValueError("key_name must be cuid, loc, locnum")
    # データベースに接続
    conn = sqlite3.connect("session.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = "SELECT * FROM {} WHERE {} = ?".format(table_name, key_name)
    cursor.execute(query, (key,))

    # レコードを取得
    records = cursor.fetchall()

    # 接続を閉じる
    conn.close()

    return records


def getrecord_fromsession(table_name, key_name, key):
    """
    指定されたテーブルから指定されたキーに一致するレコードを取得します。

    Args:
        table_name (str): テーブル名
        key_name (str): キーのカラム名
        key (str): キーの値

    Returns:
        tuple: レコードのタプル。一致するレコードがない場合はNoneを返します。
    """
    # レコードを取得
    records = getrecords_fromsession(table_name, key_name, key)
    if len(records) != 0:
        record = records[0]
    else:
        record = None

    return record


def getrecord_fromgamebasicdata(key_name, key):
    # key_nameがcid, cardname, leader, cardpack, cost, category, rarity, type, attack, hp, effect, flavorであるかどうかを判定
    if key_name not in [
        "cid",
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
    ]:
        # cid, cardname, leader, cardpack, cost, category, rarity, type, attack, hp, effect, flavorでない場合はエラー
        raise ValueError(
            "key_name must be cid, cardname, leader, cardpack, cost, category, rarity, type, attack, hp, effect, flavor"
        )
    # データベースに接続
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    # レコードを取得するSQL文を実行
    query = "SELECT * FROM card_basicdata WHERE {} = ?".format(key_name)
    cursor.execute(query, (key,))

    # レコードを取得
    record = cursor.fetchone()

    # 接続を閉じる
    conn.close()

    return record


def deletecard_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("DELETE FROM card_basicdata WHERE cid = ?", (cid,))
    con.commit()
    con.close()
    return True


def getfilename_fromfid(fid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT filename FROM card_material WHERE fid = ?", (fid,))
    filename = _card_fetchone(cur)
    con.close()
    return filename


def getfid_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT fid FROM card_basicdata WHERE cid = ?", (cid,))
    fid = _card_fetchone(cur)
    con.close()
    return fid


def getfilename_fromcid(cid):
    fid = getfid_fromcid(cid)
    filename = getfilename_fromfid(fid)
    return filename


def getfilename_fromupname(name):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT filename FROM card_material WHERE name = ?", (name,))
    filename = _card_fetchone(cur)
    con.close()
    return filename


def getcardname_fromcid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT cardname FROM card_basicdata WHERE cid = ?", (cid,))
    cardname = _card_fetchone(cur)
    con.close()
    return cardname


def getcid_fromcardname(cardname):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT cid FROM card_basicdata WHERE cardname = ?", (cardname,))
    cid = _card_fetchone(cur)
    con.close()
    return cid


def postcard(
    cid,
    fid,
    cardname,
    leader,
    cardpack,
    cost,
    category,
    rarity,
    cardtype,
    attack,
    hp,
    effect,
    flavor,
):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO card_basicdata (cid, fid, cardname, leader, cardpack, cost, category, rarity, type, attack, hp, effect, flavor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            cid,
            fid,
            cardname,
            leader,
            cardpack,
            cost,
            category,
            rarity,
            cardtype,
            attack,
            hp,
            effect,
            flavor,
        ),
    )
    con.commit()
    con.close()
    return


def isexist_cid(cid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT cid FROM card_basicdata WHERE cid = ?", (cid,))
    if _card_fetchone(cur) is None:
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
    cur.execute("SELECT * FROM card_material WHERE owneruid = ?", (uid,))
    fileinfos = cur.fetchall()
    con.close()
    return fileinfos


def deletefile_fromfilename(filename, sid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    uid = getuid_fromsid(sid)
    cur.execute(
        "SELECT * FROM card_material WHERE filename = ? AND owneruid = ?",
        (filename, uid),
    )
    if _card_fetchone(cur) is None:
        con.close()
        return False
    cur.execute(
        "DELETE FROM card_material WHERE filename = ? AND owneruid = ?", (filename, uid)
    )
    con.commit()
    con.close()
    return True


def deletefile_fromfilename_admin(filename):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM card_material WHERE filename = ?", (filename,))
    if _card_fetchone(cur) is None:
        con.close()
        return False
    cur.execute("DELETE FROM card_material WHERE filename = ?", (filename,))
    con.commit()
    con.close()
    return True


def postfile(fid, owneruid, kind, name, original_filename, filename, upload_date):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO card_material (fid, owneruid, kind, name, original_filename, filename, upload_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (fid, owneruid, kind, name, original_filename, filename, upload_date),
    )
    con.commit()
    con.close()
    return


def isexist_filename(filename):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT filename FROM card_material WHERE filename = ?", (filename,))
    if _card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def isexist_fid(fid):
    con = sqlite3.connect("game.db")
    cur = con.cursor()
    cur.execute("SELECT filename FROM card_material WHERE fid = ?", (fid,))
    if _card_fetchone(cur) is None:
        con.close()
        return False
    else:
        con.close()
        return True


def getuid_fromsid(sid):
    """
    指定されたセッションIDからユーザーIDを取得します。

    Parameters:
    sid (str): セッションID

    Returns:
    str: ユーザーID
    """
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT uid FROM usersession WHERE sid = ?", (sid,))
    uid = _card_fetchone(cur)
    con.close()
    return uid


def getnickname_fromsid(sid):
    """
    指定されたセッションIDに関連付けられたニックネームを取得します。

    Parameters:
        sid (str): セッションID

    Returns:
        str: ニックネーム
    """
    uid = getuid_fromsid(sid)
    nickname = getnickname_fromuid(uid)
    return nickname


def getnickname_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT nickname FROM user WHERE uid = ?", (uid,))
    nickname = _card_fetchone(cur)
    con.close()
    return nickname


def getemail_fromsid(sid):
    uid = getuid_fromsid(sid)
    email = getemail_fromuid(uid)
    return email


def getemail_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT email FROM user WHERE uid = ?", (uid,))
    email = _card_fetchone(cur)
    con.close()
    return email


def getsid_fromsid(sid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("SELECT sid FROM usersession WHERE sid = ?", (sid,))
    sid = _card_fetchone(cur)
    con.close()
    return sid


def postusersession(sid, uid, datestr):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "INSERT INTO usersession VALUES (?, ?, ?, ?, ?)"
    cur.execute(query, (sid, uid, datestr, "", getnickname_fromuid(uid)))
    con.commit()
    con.close()
    return


def putusersession(sid, datestr):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("UPDATE usersession SET accessdate = ? WHERE sid = ?", (datestr, sid))
    con.commit()
    con.close()
    return


def putusersession_gsid(sid, gsid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    cur.execute("UPDATE usersession SET gsid = ? WHERE sid = ?", (gsid, sid))
    con.commit()
    con.close()
    return


def deleteusersession(uid):
    con = sqlite3.connect("session.db")
    cur = con.cursor()
    query = "DELETE FROM usersession WHERE uid = ?"
    cur.execute(query, (uid,))
    con.commit()
    con.close()
    return


def getnickname_fromemail(email):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT nickname FROM user WHERE email = ?", (email,))
    nickname = _card_fetchone(cur)
    con.close()
    return nickname


def getuid_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT uid FROM user WHERE uid = ?", (uid,))
    uid = _card_fetchone(cur)
    con.close()
    return uid


def getnickname_fromnickname(nickname):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT nickname FROM user WHERE nickname = ?", (nickname,))
    nickname = _card_fetchone(cur)
    con.close()
    return nickname


def getgrant_fromuid(uid):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT grant FROM user WHERE uid = ?", (uid,))
    grant = _card_fetchone(cur)
    con.close()
    return grant


def postuser(uid, email, nickname):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    query = "INSERT INTO user VALUES (?, ?, ?, ?)"
    cur.execute(query, (uid, email, nickname, ""))
    con.commit()
    con.close()
    return


def getuid_fromemail(email):
    con = sqlite3.connect("user.db")
    cur = con.cursor()
    cur.execute("SELECT uid FROM user WHERE email = ?", (email,))
    uid = _card_fetchone(cur)
    con.close()
    return uid
