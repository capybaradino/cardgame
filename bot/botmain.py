import requests
import json
import time

base_url = "http://localhost:5001"  # Flask REST APIのベースURL
sid = "bb1a656b-3083-4735-b638-35ffe584189a"


def start_game():
    response = requests.post(f"{base_url}/system/{sid}/newgame")
    print(response.text)
    return response.status_code


def get_status():
    response = requests.get(f"{base_url}/system/{sid}/status")
    print(response.text)
    return response.status_code, response.text


def get_view():
    response = requests.get(f"{base_url}/view/{sid}")
    return response.status_code, response.text


def play_card(handno, boardno):
    print("[INFO] play card start")
    response = requests.post(
        f"{base_url}/play/{sid}/hand_{handno}/leftboard_{boardno}")
    print(response.text)
    print("[INFO] play card end")
    return response.status_code


def play_attack(cardno, boardno):
    print("[INFO] play attack start")
    response = requests.post(
        f"{base_url}/play/{sid}/leftboard_{cardno}/rightboard_{boardno}")
    print(response.text)
    print("[INFO] play attack end")
    return response.status_code


def get_result():
    response = requests.get(f"{base_url}/system/{sid}/result")
    print(response.text)
    return response.status_code


def turn_end():
    response = requests.post(f"{base_url}/system/{sid}/turnend")
    print(response.text)
    return response.status_code


def end_game():
    response = requests.post(f"{base_url}/end_game")
    print(response.json()["message"])


# 前回のゲームをクリア
print("[INFO] reset game")
get_result()

while True:
    # ゲームを開始
    print("[INFO] start game")
    ret = start_game()
    if (ret != 200):
        print("[ERROR] failed to start game")
        exit(1)

    while True:
        print("[INFO] sleep 5 sec")
        time.sleep(5)
        print("[INFO] get status")
        ret, restext = get_status()
        if (ret != 200):
            print("[ERROR] failed to get state")
            exit(1)
        data = json.loads(restext)
        if (data["status"] == "matching"):
            continue
        if (data["status"] != "playing"):
            break
        else:
            # TODO 自動プレイ
            print("[INFO] get view")
            ret, restext = get_view()
            if (ret != 200):
                print("[ERROR] failed to get view")
                break
            data = json.loads(restext)
            if (data["turn"] != "p1turn"):
                print("[INFO] turn = " + data["turn"])
                continue
            # TODO ここに実装
            # 各種データを初期化
            remainhand = True
            remainact = True
            while (remainhand or remainact):
                # TODO 暴走したときの対策
                time.sleep(1)
                ret, restext = get_view()
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
                        play_card(play_hand, play_board)
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
                        play_attack(attack_card, attack_board)
                        continue
            print("[INFO] turn end")
            ret = turn_end()
            if (ret != 200):
                print("[ERROR] failed to turn end")
                break
        continue

    print("[INFO] get result")
    ret = get_result()
    if (ret != 200):
        print("[ERROR] failed to get result")
        exit(1)

    # TODO 解放
    exit(0)
