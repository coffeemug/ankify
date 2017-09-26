
import ui
import os
import sys
import config
from anki import Collection as aopen
from anki import sync

def init(_x):
    global x
    x = _x

def synchronize():
    (client, server, hkey) = connect(x)
    ret = attempt_incremental_sync(client)
    if ret == 'fullSync':
        ret = perform_full_sync(x, server, hkey)
    print(ret)
    perform_media_sync(x, server, hkey)

###

def connect(x):
    hkey = config.hkey()
    server = sync.RemoteServer(hkey)
    hkey = authenticate(hkey, server)
    client = sync.Syncer(x, server)
    return (client, server, hkey)

def authenticate(hkey, server):
    if not hkey:
        username = ui.uinput(uprompt='Username', required=True)
        password = ui.uinput(uprompt='Password', required=True, password=True)
        print('Authenticating...', end=' ', flush=True)
        hkey = server.hostKey(username, password)
        if not hkey:
            print( "bad auth")
            raise EOFError()
        else:
            print("success")
            config.save_hkey(hkey)
    return hkey

def attempt_incremental_sync(client):
    print('Attempting incremental sync...', end=' ', flush=True)
    return client.sync()

def perform_full_sync(x, server, hkey):
    dir = ui.up_down()
    client = sync.FullSyncer(x, hkey, server.client)
    try:
        if dir == "u":
            print('Full upload...', end=' ', flush=True)
            if client.upload():
                ret = 'success'
            else:
                ret = 'err'
        else:
            print('Full download...', end=' ', flush=True)
            client.download()
            ret = 'success'
    except Exception as e:
        print(str(e))
        raise
    x.reopen()
    return ret

def perform_media_sync(x, server, hkey):
    print('Performing media sync...', end=' ', flush=True)
    server = sync.RemoteMediaServer(x, hkey, server.client)
    client = sync.MediaSyncer(x, server)
    try:
        ret = client.sync()
    except Exception as e:
        ret = str(e)
    print(ret)

