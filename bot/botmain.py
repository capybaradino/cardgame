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

def get_result():
    response = requests.get(f"{base_url}/system/{sid}/result")
    print(response.text)
    return response.status_code

def next_turn():
    response = requests.post(f"{base_url}/next_turn")
    print(response.json()["message"])

def end_game():
    response = requests.post(f"{base_url}/end_game")
    print(response.json()["message"])

while True:
    # ゲームを開始
    print("[INFO] start game")
    ret = start_game()
    if(ret != 200):
        print("[ERROR] failed to start game")
        exit(1)

    while True:
        print("[INFO] get status")
        ret, restext = get_status()
        if(ret != 200):
            print("[ERROR] failed to get state")
            exit(1)
        data = json.loads(restext)
        if(data["status"] != "playing"):
            break
        print("[INFO] sleep 5 sec")
        time.sleep(5)
        continue

    print("[INFO] get result")
    ret = get_result()
    if(ret != 200):
        print("[ERROR] failed to get result")
        exit(1)

    exit(0)
