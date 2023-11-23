import os
import sqlite3


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"ファイル '{file_path}' を削除しました。")
    except FileNotFoundError:
        print(f"ファイル '{file_path}' が見つかりません。")
    except Exception as e:
        print(f"ファイル '{file_path}' の削除中にエラーが発生しました: {e}")


def drop_table(database_name, table_name):
    try:
        # SQLite3データベースに接続
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # テーブルを削除するSQLクエリを実行
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # 変更をコミットしてデータベースを更新
        conn.commit()
        return True  # テーブルの削除が成功した場合にTrueを返す

    except sqlite3.Error as e:
        print(f"テーブルの削除中にエラーが発生しました: {e}")
        return False  # テーブルの削除が失敗した場合にFalseを返す

    finally:
        # データベースとの接続を閉じる
        conn.close()


def create_database(db_name):
    try:
        # データベースに接続（存在しない場合は新規作成される）
        conn = sqlite3.connect(db_name)
        print(f"データベース '{db_name}' を作成しました。")
        conn.close()
    except Exception as e:
        print(f"データベースの作成中にエラーが発生しました: {e}")


def create_table(db_name, table_name):
    try:
        # データベースに接続（存在しない場合は新規作成される）
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # テーブルの作成
        if table_name == "card_basicdata":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    cid TEXT PRIMARY KEY,
                    fid TEXT NOT NULL,
                    cardname TEXT NOT NULL,
                    leader TEXT NOT NULL,
                    cardpack TEXT NOT NULL,
                    cost INTEGER,
                    category TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    type TEXT,
                    attack INTEGER,
                    hp INTEGER,
                    effect TEXT,
                    flavor TEXT
                )
            """
        if table_name == "card_material":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    fid TEXT PRIMARY KEY,
                    owneruid TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    name TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    upload_date TEXT NOT NULL
                )
            """
        if table_name == "user":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    uid TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    nickname TEXT NOT NULL,
                    grant TEXT
                )
            """
        if table_name == "usersession":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    sid TEXT PRIMARY KEY,
                    uid TEXT NOT NULL,
                    accessdate TEXT NOT NULL,
                    gsid TEXT NOT NULL,
                    name TEXT NOT NULL
                )
            """
        if table_name == "gamesession":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    gsid TEXT PRIMARY KEY,
                    p1_player_tid TEXT NOT NULL,
                    p2_player_tid TEXT NOT NULL,
                    card_table TEXT NOT NULL,
                    log TEXT NOT NULL,
                    state TEXT NOT NULL,
                    lastupdate TEXT NOT NULL
                )
            """
        if table_name == "playerstats":
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    player_tid TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    job TEXT NOT NULL,
                    hp INTEGER NOT NULL,
                    mp INTEGER NOT NULL,
                    maxmp INTEGER NOT NULL,
                    tension INTEGER NOT NULL,
                    skillboost INTEGER NOT NULL,
                    fatigue INTEGER NOT NULL,
                    rsv2 TEXT,
                    rsv3 TEXT,
                    rsv4 TEXT,
                    rsv5 TEXT,
                    rsv6 TEXT,
                    rsv7 TEXT,
                    rsv8 TEXT
                )
            """
        cursor.execute(query)

        conn.commit()
        conn.close()
        print(f"テーブル '{table_name}' をデータベース '{db_name}' 内に作成しました。")
    except Exception as e:
        print(f"テーブルの作成中にエラーが発生しました: {e}")


def drop_tables_with_prefix(database_name, prefix):
    try:
        # SQLite3データベースに接続
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # データベース内のテーブル一覧を取得
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # テーブル名が指定の接頭辞で始まる場合、それらのテーブルを削除
        for table in tables:
            table_name = table[0]
            if table_name.startswith(prefix):
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # 変更をコミットしてデータベースを更新
        conn.commit()
        return True  # テーブルの削除が成功した場合にTrueを返す

    except sqlite3.Error as e:
        print(f"テーブルの削除中にエラーが発生しました: {e}")
        return False  # テーブルの削除が失敗した場合にFalseを返す

    finally:
        # データベースとの接続を閉じる
        conn.close()


# main start
print("[INFO] Select db to initialize.")
print(
    "       1:game.db 2:user.db 3:session.db 4:sesstable(not user) 5:sesstable(user) A:ALL C:Cancel"
)
str = input()

if str == "C":
    exit()

print("[INFO] Initialize db start.")

# game.db
if str == "1" or str == "A":
    dbfile_path = "game.db"
    delete_file(dbfile_path)
    create_database(dbfile_path)
    table_name = "card_basicdata"
    create_table(dbfile_path, table_name)
    table_name = "card_material"
    create_table(dbfile_path, table_name)

# user.db
if str == "2" or str == "A":
    dbfile_path = "user.db"
    delete_file(dbfile_path)
    create_database(dbfile_path)
    table_name = "user"
    create_table(dbfile_path, table_name)

# session.db
if str == "3" or str == "A":
    dbfile_path = "session.db"
    delete_file(dbfile_path)
    create_database(dbfile_path)
    table_name = "usersession"
    create_table(dbfile_path, table_name)
    table_name = "gamesession"
    create_table(dbfile_path, table_name)
    table_name = "playerstats"
    create_table(dbfile_path, table_name)

# session.db(not user)
if str == "4" or str == "A":
    dbfile_path = "session.db"
    table_name = "gamesession"
    drop_table(dbfile_path, table_name)
    create_table(dbfile_path, table_name)
    table_name = "playerstats"
    drop_table(dbfile_path, table_name)
    create_table(dbfile_path, table_name)
    # 残存カード管理テーブルの削除
    drop_tables_with_prefix(dbfile_path, "c_")

# session.db(user)
if str == "5" or str == "A":
    dbfile_path = "session.db"
    table_name = "usersession"
    drop_table(dbfile_path, table_name)
    create_table(dbfile_path, table_name)


print("[INFO] Initialize db end.")
