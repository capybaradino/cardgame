from class_playview import Play_view


# 勝敗を判定する
def judge(sid):
    playview = Play_view(sid)
    if playview.p1hp <= 0:
        playview.playdata.gameover(sid)
    if playview.p2hp <= 0:
        playview.playdata.gamewin(sid)
    return
