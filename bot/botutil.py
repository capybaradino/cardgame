def search_rightboard(p2board):
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
    return attack_board
