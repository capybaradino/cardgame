import os
import sqlite3


def update_table(db_name, table_name, key_name, key, column, value):
    try:
        # Connect to the database (create a new one if it doesn't exist)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        query = f"UPDATE {table_name} SET {column} = ? WHERE {key_name} = ?"
        cursor.execute(query, (value, key))
        conn.commit()
        conn.close()
        print(f"Updated table '{table_name}'.")
    except Exception as e:
        print(f"Error occurred while updating the table: {e}")


# 参照モード
def view_mode():
    # どのdbを参照するか選択させる
    print("[INFO] Select db to view.")
    print("       1:game.db 2:user.db 3:session.db C:Cancel")
    strinput = input()

    if strinput == "C":
        return "C"

    print("[INFO] View db start.")

    if strinput == "2":
        # user.dbの情報を表示
        con = sqlite3.connect("user.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM user")
        records = cur.fetchall()
        for record in records:
            print(record)
        con.close()

    if strinput == "3":
        # どのテーブルを参照するか選択させる
        print("[INFO] Select table to view.")
        print("       1:usersession 2:gamesession 3:playerstats C:Cancel")
        strinput = input()

        if strinput == "1":
            # usersessionの情報を表示
            con = sqlite3.connect("session.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM usersession")
            records = cur.fetchall()
            for record in records:
                print(record)
            con.close()

        if strinput == "2":
            # gamesessionの情報を表示
            con = sqlite3.connect("session.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM gamesession")
            records = cur.fetchall()
            for record in records:
                print(record)
            con.close()

        if strinput == "3":
            # playerstatsの情報を表示
            con = sqlite3.connect("session.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM playerstats")
            records = cur.fetchall()
            for record in records:
                print(record)
            con.close()

    print("[INFO] View db end.")
    return ""


# 更新モード
def update_mode():
    # どのdbを更新するか選択させる
    print("[INFO] Select db to update.")
    print("       1:game.db 2:user.db 3:session.db C:Cancel")
    strinput = input()

    if strinput == "C":
        return "C"

    print("[INFO] Update db start.")

    # user.db
    if strinput == "2":
        print("[INFO] Input nickname:")
        key = input()
        print("[INFO] Input grant(admin/[empty]):")
        value = input()
        dbfile_path = "user.db"
        table_name = "user"
        update_table(dbfile_path, table_name, "nickname", key, "grant", value)

    if strinput == "M":
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

    print("[INFO] Update db end.")
    return ""


# main start
def main():
    # 参照モードかアップデートモードか選択させる
    print("[INFO] Select mode.")
    print("       1:View 2:Update C:Cancel")
    strinput = input()

    if strinput == "1":
        # 無限ループ
        while True:
            ret = view_mode()
            if ret == "C":
                break

    if strinput == "2":
        # 無限ループ
        while True:
            ret = update_mode()
            if ret == "C":
                break

    if strinput == "C":
        exit()

    return


if __name__ == "__main__":
    # 全体をループさせる
    while True:
        main()
