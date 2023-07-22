import sqlite3
import os

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"ファイル '{file_path}' を削除しました。")
    except FileNotFoundError:
        print(f"ファイル '{file_path}' が見つかりません。")
    except Exception as e:
        print(f"ファイル '{file_path}' の削除中にエラーが発生しました: {e}")

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
        if(table_name == 'card_basicdata'):
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
        cursor.execute(query)

        conn.commit()
        conn.close()
        print(f"テーブル '{table_name}' をデータベース '{db_name}' 内に作成しました。")
    except Exception as e:
        print(f"テーブルの作成中にエラーが発生しました: {e}")

print("[INFO] This will initialize all db. Are you sure to continue? (y/n)")

str = input()

if(str != 'y'):
    exit()

print("[INFO] Initialize db start.")

dbfile_path = 'game.db'
delete_file(dbfile_path)
create_database(dbfile_path)
table_name = 'card_basicdata'
create_table(dbfile_path, table_name)

print("[INFO] Initialize db end.")
