import configparser
import debug

def getparam(key):
    debugparam = debug.getdebugparam(key)
    if(debugparam is not None):
        return debugparam
    else:
        conf = configparser.ConfigParser()
        conf.read("game.ini")
        section = "player"
        return conf.get(section, key)
