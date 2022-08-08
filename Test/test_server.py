import pytest
from Client.app_clients import AppClient
import torch.nn as nn
import socket
import time
import sys
sys.path.insert(0,"..")
import threading
import yaml

from Server.app_servers import AppServer
conf = None
with open('server_conf.yml') as f:
    conf = yaml.safe_load(f)



@pytest.fixture
def start_server():
    app = AppServer('server_conf.yml')
    app.run()

@pytest.fixture
def finish():
    yield
    sys.exit()


def test_server_datachannel_conn(start_server):
    threading.Thread(target = start_server).start()

    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    err = None
    time.sleep(conf['datachannel_time_interval'] + 1)
    try:
        s.connect((conf['ip'], conf['datachannel_port']))
    except socket.error as e:
        err = e
    
    assert err == None

def test_server_ping_conn(finish):
    threading.Thread(target = start_server).start()

    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    err = None
    try:
        s.connect((conf['ip'], conf['ping_port']))
    except socket.error as e:
        err = e
    
    assert err == None

