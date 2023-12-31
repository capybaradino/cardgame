import sqlite3
from datetime import datetime

import card_db
import game


def cleanupPlayerstats():
    # playerstats上のname重複ありの場合の処理
    maxcnt = 10
    i = 0
    while i < maxcnt:
        playerstats = card_db.getallplayerstats()
        foundDuplicate = False
        for playerstat in playerstats:
            tid = playerstat[0]
            name = playerstat[1]
            for playerstat in playerstats:
                # 自分自身は除外
                if tid == playerstat[0]:
                    continue
                if name == playerstat[1]:
                    # 重複検出、このnameを持つplayerstatを全削除
                    for playerstat in playerstats:
                        card_db.deleteplayerstats(playerstat[0])
                    foundDuplicate = True
                    break
            # 重複が見つかった場合は一度ループを抜けDBを再読み込み
            if foundDuplicate:
                break
        # 重複が見つからなかった場合はループを抜ける
        if not foundDuplicate:
            break
        i += 1
    # gamesession視点での整合性チェック
    gamesessions = card_db.getallgamesessions()
    for gamesession in gamesessions:
        gsid = gamesession[0]
        p1_player_tid = gamesession[1]
        p2_player_tid = gamesession[2]
        card_table = gamesession[3]
        playerstats = card_db.getplayerstats_bytid(p1_player_tid)
        # player_tidがplayerstatsに存在しない場合は削除
        if playerstats is None:
            card_db.deletegamesession(gsid)
            card_db.deletedecktable(card_table)
            continue
        playerstats = card_db.getplayerstats_bytid(p2_player_tid)
        if playerstats is None and p2_player_tid != "waiting":
            card_db.deletegamesession(gsid)
            card_db.deletedecktable(card_table)
            continue
    # playerstats視点での整合性チェック
    playerstats = card_db.getallplayerstats()
    for playerstat in playerstats:
        # player_tidがgamesessionに存在しない場合は削除
        tid = playerstat[0]
        gamesession1 = card_db.getgamesession("p1_player_tid", tid)
        gamesession2 = card_db.getgamesession("p2_player_tid", tid)
        if gamesession1 is None and gamesession2 is None:
            card_db.deleteplayerstats(tid)


def _getnamefromtid(gamesession):
    p1_player_tid = gamesession[1]
    p2_player_tid = gamesession[2]
    p1_player_name = card_db.getplayerstats_bytid(p1_player_tid)[1]
    if p2_player_tid != "waiting":
        p2_player_name = card_db.getplayerstats_bytid(p2_player_tid)[1]
    else:
        p2_player_name = "waiting"
    return p1_player_name, p2_player_name


def _gettidfromname(player_name):
    record = card_db.getplayerstats_byname(player_name)
    if record is None:
        return None
    return record[0]


def card_getwaitingsessionhtml(username):
    # TODO 実行契機見直し
    cleanupPlayerstats()
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
    # 全ゲームセッションを取得する
    gamesessions = card_db.getallgamesessions()
    if gamesessions is None:
        return headers
    for gamesession in gamesessions:
        # player1またはplayer2に自分の名前がある場合は表示
        p1_player_name, p2_player_name = _getnamefromtid(gamesession)
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
            headers += "<td>" + msg + "</td>"
            headers += "</tr>"
            isMatchExist = True

    for gamesession in gamesessions:
        gsid = gamesession[0]
        # player1またはplayer2に自分の名前がある場合は非表示
        p1_player_name, p2_player_name = _getnamefromtid(gamesession)
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


def card_getdatestrnow():
    dt_now = datetime.now()
    return _card_getdatestr(dt_now)


def _card_getdatestr(dt):
    return dt.isoformat()


def card_settimer(p1name, p2name, turnstate):
    if turnstate == "p1turn":
        # Player1のturnstarttimeを削除し、Player2のturnstarttimeを設定
        card_db.putplayerstats("name", p1name, "turnstarttime", "")
        card_db.putplayerstats("name", p2name, "turnstarttime", card_getdatestrnow())
    else:
        # Player2のturnstarttimeを削除し、Player1のturnstarttimeを設定
        card_db.putplayerstats("name", p2name, "turnstarttime", "")
        card_db.putplayerstats("name", p1name, "turnstarttime", card_getdatestrnow())


def card_gettimeoutvalue():
    # 制限時間(秒)を取得
    turntimeout = int(game.getparam("turntimeout"))
    return turntimeout


def card_istimeout(datestr1, datestr2):
    dt1 = datetime.fromisoformat(datestr1)
    dt2 = datetime.fromisoformat(datestr2)
    # 制限時間(秒)を取得
    turntimeout = card_gettimeoutvalue()
    # 時間差を取得
    timedelta = dt2 - dt1
    # 時間差が制限時間を超えている場合はTrue
    return timedelta.total_seconds() > turntimeout
