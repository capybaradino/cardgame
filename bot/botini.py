import configparser
import os

def getdebugparam(key):
    is_file = os.path.isfile("bot.conf")
    if is_file:
        conf = configparser.ConfigParser()
        conf.read("bot.conf")
        section = "param"
        return conf.get(section, key)
    else:
        return None