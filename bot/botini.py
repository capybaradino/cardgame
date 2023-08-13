import configparser
import os


def getcardhome():
    value = os.environ.get('CARD_HOME')
    return value


def getdebugparam(key):
    value = getcardhome()
    conf_path = ""
    if value is not None:
        conf_path = value + "/bot/bot.conf"
    else:
        conf_path = "bot.conf"
    is_file = os.path.isfile(conf_path)
    if is_file:
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        section = "param"
        return conf.get(section, key)
    else:
        return None
