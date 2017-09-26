
import sys
import os.path
import configparser

conf_path = os.path.expanduser('~/tanki.ini')
conf = None

def init():
    if os.path.isfile(conf_path):
        return

    global conf
    conf  = configparser.ConfigParser()
    conf['settings'] = {
        'db': '~/Library/Application Support/Anki2/User 1/collection.anki2',
    }
    save()

def db_path():
    return os.path.expanduser(load()['settings']['db'])

def hkey():
    return load()['settings'].get('hkey')


def save_hkey(val):
    load()['settings']['hkey'] = val
    save()

###
def load():
    global conf
    if conf:
        return conf
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    return conf

def save():
    global conf
    with open(conf_path, 'w') as configfile:
        conf.write(configfile)
