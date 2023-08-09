import configparser
import os

def getdebugparam(key):
    is_file = os.path.isfile("debug.conf")
    if is_file:
        conf = configparser.ConfigParser()
        conf.read("debug.conf")
        section = "debug"
        return conf.get(section, key)
    else:
        return None