import json
import time
import botini
from botsub import Botsub

base_url = ""  # Flask REST APIのベースURL
sid = ""


def run():

    # iniファイル読み込み
    polling_interval_sec = int(botini.getdebugparam("polling_interval_sec"))
    command_interval_sec = int(botini.getdebugparam("command_interval_sec"))
    exec_mode = botini.getdebugparam("exec_mode")   # daemon/onetime
    base_url = botini.getdebugparam("base_url")
    sid = botini.getdebugparam("sid")

    sub = Botsub(base_url, sid)

    # 前回のゲームをクリア
    print("[INFO] reset game")
    sub.surrender()
    sub.get_result()

    while True:
        # ゲームを開始
        print("[INFO] start game")
        ret = sub.start_game()
        if (ret != 200):
            print("[ERROR] failed to start game")
            exit(1)

        while True:
            print("[INFO] sleep 5 sec")
            time.sleep(polling_interval_sec)
            print("[INFO] get status")
            ret, restext = sub.get_status()
            if (ret != 200):
                print("[ERROR] failed to get state")
                exit(1)
            data = json.loads(restext)
            if (data["status"] == "matching"):
                continue
            if (data["status"] != "playing"):
                break
            else:
                # 自動プレイ
                print("[INFO] get view")
                ret, restext = sub.get_view()
                if (ret != 200):
                    print("[ERROR] failed to get view")
                    break
                data = json.loads(restext)
                if (data["turn"] != "p1turn"):
                    print("[INFO] turn = " + data["turn"])
                    continue

                # 各種データを初期化
                remainhand = True
                remainact = True
                while (remainhand or remainact):
                    # TODO 暴走したときの対策
                    time.sleep(command_interval_sec)
                    ret, restext = sub.get_view()
                    if (ret != 200):
                        break
                    data = json.loads(restext)
                    player1 = data["player1"]
                    mp = player1["MP"]
                    hand = player1["hand"]
                    board = player1["board"]
                    player2 = data["player2"]
                    p2board = player2["board"]
                    if (ret != 200):
                        print("[ERROR] failed to get view")
                        break
                    # ハンド確認
                    if (remainhand):
                        # ハンドを探す
                        i = 0
                        play_hand = -1
                        for card in hand:
                            if (card["cost"] <= mp):
                                play_hand = i
                                break
                            i = i + 1
                        if (play_hand < 0):
                            # ハンドから出せるユニットがいない
                            remainhand = False
                        # 空き盤面を探す
                        i = 0
                        play_board = -1
                        while (i < 6):
                            empty = True
                            for card in board:
                                if (card["location"] == i):
                                    empty = False
                            if (empty):
                                play_board = i
                                break
                            i = i + 1
                        if (play_board < 0):
                            # 盤面が空いていない
                            remainhand = False
                        if (remainhand):
                            # プレイ
                            sub.play_card(play_hand, play_board)
                            continue
                    if (remainact):
                        # 行動するユニットを選択
                        attack_card = -1
                        for card in board:
                            if (card["active"] > 0):
                                attack_card = card["location"]
                        # 対象ユニットがいない
                        if (attack_card < 0):
                            remainact = False
                        # 相手の盤面を検索
                        attack_board = -1
                        for card in p2board:
                            # 前衛を優先して攻撃
                            if (card["location"] < 3):
                                attack_board = card["location"]
                        if (attack_board < 0):
                            for card in p2board:
                                # 前衛がいない場合は後衛を攻撃
                                attack_board = card["location"]
                        # 対象盤面がいない場合はリーダーを攻撃
                        if (attack_board < 0):
                            attack_board = 10
                        if (remainact):
                            # 攻撃
                            sub.play_attack(attack_card, attack_board)
                            continue
                print("[INFO] turn end")
                ret = sub.turn_end()
                if (ret != 200):
                    print("[ERROR] failed to turn end")
                    break
            continue

        print("[INFO] get result")
        ret = sub.get_result()
        if (ret != 200):
            print("[ERROR] failed to get result")
            exit(1)

        # 解放
        if (exec_mode == "onetime"):
            exit(0)


# Omajinai
if __name__ == "__main__":
    run()
