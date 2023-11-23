import configparser
import os

import debug


def getparam(key):
    debugparam = debug.getdebugparam(key)
    if debugparam is not None:
        return debugparam
    else:
        conf = configparser.ConfigParser()
        if os.path.isfile("game.ini"):
            game_ini = "game.ini"
        else:
            game_ini = "game_sample.ini"
        conf.read(game_ini)
        section = "player"
        return conf.get(section, key)
