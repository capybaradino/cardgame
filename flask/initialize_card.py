import csv
import sqlite3
import uuid


def card_fetchone(cur):
    item = cur.fetchone()
    if (item is not None):
        item = item[0]
    return item


def isexist_cid(cid):
    con = sqlite3.connect('game.db')
    cur = con.cursor()
    cur.execute(
        "select cid from card_basicdata where cid = '" + cid + "'")
    if (card_fetchone(cur) is None):
        con.close()
        return False
    else:
        con.close()
        return True


class Csvcard():
    def __init__(self, originalname, newname, effect):
        self.name = newname

        with open('gamecard.csv', 'r') as file:
            reader = csv.reader(file, delimiter='\t')  # タブ区切りのCSVとして読み込む

            row = next(reader)
            # print(row)
            i = 0
            for col in row:
                if col == "カード名3":
                    CARD_NAME = i
                if col == "職業":
                    LEADER = i
                if col == "カードパック":
                    CARD_PACK = i
                if col == "コスト":
                    COST = i
                if col == "種類":
                    CATEGORY = i
                if col == "レア度":
                    RARITY = i
                if col == "系統":
                    TYPE = i
                if col == "攻撃力":
                    ATTACK = i
                if col == "体力":
                    HP = i
                if col == "おうえん":
                    EFFECT = i
                i = i + 1

            flg = 0
            for row in reader:
                if row[CARD_NAME] == originalname:
                    print(row)
                    if row[LEADER] == "共通":
                        self.leader = "common"
                    elif row[LEADER] == "魔法使い":
                        self.leader = "wiz"
                    elif row[LEADER] == "武闘家":
                        self.leader = "mnk"
                    else:
                        print("[ERROR] Leader " +
                              row[LEADER] + " is not defined.")
                        exit(1)

                    if row[CARD_PACK] == "00ベーシック":
                        self.cardpack = "00basic"
                    elif row[CARD_PACK] == "01スタンダード":
                        self.cardpack = "01standard"
                    elif row[CARD_PACK] == "02力の咆哮":
                        self.cardpack = "02power"
                    elif row[CARD_PACK] == "xx":
                        self.cardpack = "standard"
                    elif row[CARD_PACK] == "xx":
                        self.cardpack = "standard"
                    elif row[CARD_PACK] == "xx":
                        self.cardpack = "standard"
                    elif row[CARD_PACK] == "xx":
                        self.cardpack = "standard"
                    self.cost = row[COST]

                    if row[CATEGORY] == "ユニット":
                        self.category = "unit"
                    elif row[CATEGORY] == "特技":
                        self.category = "spell"

                    if row[RARITY] == "0":
                        self.rarity = "common"
                    elif row[RARITY] == "1":
                        self.rarity = "rare"
                    elif row[RARITY] == "2":
                        self.rarity = "super"
                    elif row[RARITY] == "3":
                        self.rarity = "legend"

                    # TODO 系統
                    self.type = ""
                    self.attack = row[ATTACK]
                    self.hp = row[HP]
                    # TODO 効果
                    self.effect = effect
                    # TODO フレーバーテキスト
                    self.flavor = ""
                    flg = 1
                    break

            if flg == 0:
                print("[ERROR] Cardname " + originalname + "not found")
                exit(1)


if __name__ == "__main__":

    print("[INFO] Select table to create.")
    print("       1:card_basicdata 2:deck C:Cancel")
    opt = input()

    if (opt == 'C'):
        exit()

    # print("[INFO] Create card data start.")

    if opt == '1':
        print("[INFO] Create card basic data start.")

        # SQLite3データベースに接続
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        # 削除したいテーブルの名前を指定
        table_name = 'card_basicdata'
        # テーブルを削除するSQLクエリを実行
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        # テーブルの作成
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
        # 変更をコミットしてデータベースを更新
        conn.commit()
        # データベースとの接続を閉じる
        conn.close()

        print("[INFO] Create cards according to csv file")
        with open('gamecard_define.csv', 'r') as file:
            reader = csv.reader(file, delimiter='\t')  # タブ区切りのCSVとして読み込む

            row = next(reader)
            print(row)
            i = 0
            for row in reader:
                originalname = row[0]
                newname = row[1]
                effect = row[2]
                newcard = Csvcard(originalname, newname, effect)

                # カードをDBに登録
                # TODO ファイル名暫定対応
                fid = "test/" + newname + ".png"
                cardname = newname

                leader = newcard.leader
                cardpack = newcard.cardpack
                cost = newcard.cost
                category = newcard.category
                rarity = newcard.rarity
                type = newcard.type
                attack = newcard.attack
                hp = newcard.hp
                effect = newcard.effect
                flavor = newcard.flavor
                while True:
                    cid = str(uuid.uuid4())
                    if (isexist_cid(cid)):
                        continue
                    break

                con = sqlite3.connect('game.db')
                cur = con.cursor()
                cur.execute("insert into card_basicdata values ('" + cid + "','" +
                            fid + "','" + cardname + "','" + leader + "','" + cardpack + "','" +
                            cost + "','" + category + "','" + rarity + "','" + type + "','" +
                            attack + "','" + hp + "','" + effect + "','" + flavor + "')")
                con.commit()
                con.close()

        print("[INFO] Create tension card")
        cid = "systemcid_tension"
        fid = "system/tension.png"
        cardname = "tension"
        leader = "common"
        cardpack = "00basic"
        cost = "1"
        category = "tension"
        rarity = "common"
        type = ""
        attack = ""
        hp = ""
        effect = ""
        flavor = ""

        con = sqlite3.connect('game.db')
        cur = con.cursor()
        cur.execute("insert into card_basicdata values ('" + cid + "','" +
                    fid + "','" + cardname + "','" + leader + "','" + cardpack + "','" +
                    cost + "','" + category + "','" + rarity + "','" + type + "','" +
                    attack + "','" + hp + "','" + effect + "','" + flavor + "')")
        con.commit()
        con.close()
        print("[INFO] Create card basic data end.")

    if opt == '2':
        print("[INFO] Create deck data start.")

        # TODO デッキ名
        deck_names = []
        deck_names.append("gamecard_wiz_2018haru_3_aguzesi")
        deck_names.append("gamecard_mnk_2018haru_2_butoka")

        for deck_name in deck_names:
            # SQLite3データベースに接続
            conn = sqlite3.connect('game.db')
            cursor = conn.cursor()
            # 削除したいテーブルの名前を指定
            table_name = deck_name
            # テーブルを削除するSQLクエリを実行
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            # 変更をコミットしてデータベースを更新
            conn.commit()
            # データベースとの接続を閉じる
            conn.close()

            # テーブル作成
            db_name = "game.db"
            table_name = deck_name
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            # テーブルの作成
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    cid TEXT NOT NULL,
                    cardname TEXT NOT NULL
                )
            """
            cursor.execute(query)
            conn.commit()
            conn.close()

            with open(deck_name + '.csv', 'r') as file:
                reader = csv.reader(file, delimiter='\t')  # タブ区切りのCSVとして読み込む

                i = 0
                for row in reader:
                    print(row)

                    with open('gamecard_define.csv', 'r') as file:
                        # タブ区切りのCSVとして読み込む
                        reader2 = csv.reader(file, delimiter='\t')

                        row2 = next(reader2)
                        # print(row)
                        flg = 0
                        for row2 in reader2:
                            if row2[0] == row[0]:
                                cardname = row2[1]
                                flg = 1
                                break
                        if flg == 0:
                            print("[ERROR] Card " + row[0] + " not found.")
                            exit(1)

                    con = sqlite3.connect(db_name)
                    cur = con.cursor()
                    query = f"""
                        SELECT cid FROM card_basicdata WHERE cardname = '{cardname}'
                    """
                    cur.execute(query)
                    cid = card_fetchone(cur)
                    if (cid is None):
                        con.close()
                        print("[ERROR] Card " + cardname + " not found.")
                        exit(1)
                    con.close()

                    con = sqlite3.connect(db_name)
                    cur = con.cursor()
                    query = f"""
                        INSERT INTO {table_name} values (?, ?)
                    """
                    cur.execute(query, (cid, cardname))
                    con.commit()
                    con.close()
        print("[INFO] Create deck data end.")
