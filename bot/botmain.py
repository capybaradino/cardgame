import json
import time
import botini
from botsub import Botsub
import logging
import botutil

base_url = ""  # Flask REST APIのベースURL
sid = ""


def run():
    # ログの設定
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    # ロガーの取得
    logger = logging.getLogger(__name__)

    # ファイルハンドラを追加
    value = botini.getcardhome()
    if value is not None:
        file_handler = logging.FileHandler(f'{value}/cardbot.log')
    else:
        file_handler = logging.FileHandler('../cardbot.log')
    file_handler.setLevel(logging.DEBUG)  # ログの出力レベルを設定
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(file_handler)

    # 標準出力ハンドラを追加
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)  # ログの出力レベルを設定
    # console_handler.setFormatter(
    #     logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    # logger.addHandler(console_handler)

    # iniファイル読み込み
    polling_interval_sec = int(botini.getdebugparam("polling_interval_sec"))
    command_interval_sec = int(botini.getdebugparam("command_interval_sec"))
    exec_mode = botini.getdebugparam("exec_mode")   # daemon/onetime
    base_url = botini.getdebugparam("base_url")
    sid = botini.getdebugparam("sid")

    sub = Botsub(base_url, sid, logger)

    # 前回のゲームをクリア
    logger.info("reset game")
    sub.surrender()
    sub.get_result()

    while True:
        # ゲームを開始
        ret = sub.start_game()
        if (ret != 200):
            print("[ERROR] failed to start game")
            exit(1)

        turn_state = ""
        turn_state_counter = 0
        while True:
            # logger.info(f"sleep {polling_interval_sec} sec")
            time.sleep(polling_interval_sec)
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
                ret, restext = sub.get_view()
                if (ret != 200):
                    logger.error("failed to get view A")
                    break
                data = json.loads(restext)
                current_turn = data["turn"]
                if (current_turn != turn_state):
                    turn_state = current_turn
                    turn_state_counter = 0
                else:
                    turn_state_counter = turn_state_counter + 1
                if (turn_state_counter < 3):
                    logger.info("turn = " + data["turn"])
                if (current_turn != "p1turn"):
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
                        logger.error("failed to get view B")
                        break
                    # ハンド確認
                    if (remainhand):
                        # ハンドを探す
                        i = 0
                        play_hand = -1
                        for card in hand:
                            if (card["cost"] <= mp):
                                # TODO 特技カード使用
                                if (card["category"] == "unit"):
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
                            # エフェクトの確認
                            isplay = 0
                            effect_array = hand[play_hand]["effect"].split(",")
                            for effect in effect_array:
                                if effect.startswith("onplay"):
                                    # TODO 召喚時効果のバリエーション実装
                                    if "dmg" in effect:
                                        # 攻撃対象の選択
                                        attack_board = botutil.search_rightboard(
                                            p2board)
                                        if (attack_board >= 0):
                                            sub.play_card_and_attack(
                                                play_hand, play_board, attack_board)
                                            isplay = 1
                            if (isplay == 0):
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
                        if (remainact):
                            # 攻撃対象の選択
                            attack_board = botutil.search_rightboard(p2board)
                            if (remainact & attack_board >= 0):
                                # 攻撃
                                sub.play_attack(attack_card, attack_board)
                                continue
                ret = sub.turn_end()
                if (ret != 200):
                    logger.error("failed to turn end")
                    break
            continue

        logger.info("get result")
        ret = sub.get_result()
        if (ret != 200):
            logger.error("failed to get result")
            exit(1)

        # 解放
        if (exec_mode == "onetime"):
            exit(0)


# Omajinai
if __name__ == "__main__":
    run()
