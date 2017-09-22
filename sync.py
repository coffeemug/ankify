
from anki import Collection as aopen
from anki import sync
import ui
import os
import sys

def synchronize(x):
    (client, server, hkey) = connect(x)
    ret = attempt_incremental_sync(client)
    if ret == 'fullSync':
        perform_full_sync()
    else:
        print(ret)
    perform_media_sync(x, server, hkey)

def attempt_incremental_sync(client):
    print('Attempting incremental sync...')
    return client.sync()

def connect(x):
    # TODO: implement hkey storage
    hkey = None
    server = sync.RemoteServer(hkey)
    if not hkey:
        username = ui.uinput(uprompt='Username', required=True)
        password = ui.uinput(uprompt='Password', required=True)
        print('Authenticating...')
        hkey = server.hostKey(username, password)
    if not hkey:
        print( "Bad auth")
        raise EOFError()
    client = sync.Syncer(x, server)
    return (client, server, hkey)

def perform_full_sync():
    # TODO: implement
    # We'll need a user decision (up or down)
    print("Full sync required, but not implemented")
    raise EOFError()

def perform_media_sync(x, server, hkey):
    print('Performing media sync...')
    server = sync.RemoteMediaServer(x, hkey, server.client)
    client = sync.MediaSyncer(x, server)
    try:
        ret = client.sync()
    except Exception as e:
        ret = str(e)
    print(ret)

if __name__ == '__main__':
    # TODO: remove this; hook up to main
    db_path = os.path.expanduser('~/Library/Application Support/Anki2/User 1/collection.anki2')
    x = aopen(db_path)
    synchronize(x)
