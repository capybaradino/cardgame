import sqlite3
import os


def update_table(db_name, table_name, key_name, key, column, value):
    try:
        # データベースに接続（存在しない場合は新規作成される）
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = f"UPDATE {table_name} SET {column} = ? WHERE {key_name} = ?"
        cursor.execute(query, (value, key))
        conn.commit()
        conn.close()
        print(f"テーブル '{table_name}' を更新しました。")
    except Exception as e:
        print(f"テーブルの更新中にエラーが発生しました: {e}")


# main start
print("[INFO] Select db to update.")
print("       1:game.db 2:user.db 3:session.db M:manual C:Cancel")
str = input()

if str == "C":
    exit()

print("[INFO] Update db start.")

# user.db
if str == "2":
    print("[INFO] Input nickname:")
    key = input()
    print("[INFO] Input grant(admin/[empty]):")
    value = input()
    dbfile_path = "user.db"
    table_name = "user"
    update_table(dbfile_path, table_name, "nickname", key, "grant", value)

if str == "M":
    print("[INFO] Input db name:")
    dbfile_path = input()
    print("[INFO] Input table_name:")
    table_name = input()
    print("[INFO] Input key_name:")
    key_name = input()
    print("[INFO] Input key:")
    key = input()
    print("[INFO] Input column:")
    column = input()
    print("[INFO] Input value:")
    value = input()
    update_table(dbfile_path, table_name, key_name, key, column, value)

print("[INFO] Initialize db end.")
