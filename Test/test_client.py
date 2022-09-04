import sys
sys.path.insert(0,"../")
import socket
from Client.app_clients import AppClient
import torch.nn as nn
import time
import threading
from Server.utils import *
import os
import yaml


ping_server = None
datachannel_server = None
connected_client_socket = None

conf = None
with open('server_conf.yml') as f:
    conf = yaml.safe_load(f)


def bind_ping_server():
    global ping_server
    ping_server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    ping_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ping_server.bind(("127.0.0.1", 9950))
    ping_server.listen(100)

def bind_datachannel_server():
    global datachannel_server
    datachannel_server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    datachannel_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    datachannel_server.settimeout(conf['datachannel_gap_time'])
    datachannel_server.bind(("127.0.0.1", 9951))
    datachannel_server.listen(100)


def start_client(conf_path):
    time.sleep(2)
    loss = nn.MSELoss()
    app = AppClient(conf_path,loss)
    app.run()

def test_client_connect_with_id():
    global connected_client_socket
    threading.Thread(target=start_client, args=("id_test/client_conf1.yml",)).start()
    connected_client_socket, _ = ping_server.accept()

    try:
        message = connected_client_socket.recv(1024).decode()
        assert message == 'Connecting with id:f4f35d119d7cd5df3f5a327c92ccc107'
    except:
        assert False

def test_client_connect_without_id():
    threading.Thread(target=start_client, args=("id_test/client_conf2.yml",)).start()
    client_socket, _ = ping_server.accept()

    try:
        message = client_socket.recv(1024).decode()
        assert message == 'Give me an id you son of a bitch!'
    except:
        assert False

def test_client_version():
    global connected_client_socket
    connected_client_socket.send(b'Oh I know you!')
    try:
        message = connected_client_socket.recv(1024).decode()
        assert message.isdecimal()
        vers = int(message) + 1

        connected_client_socket.send(b'update')
        message = connected_client_socket.recv(1024).decode()
        assert message == 'Send version and model'

        connected_client_socket.send(str(vers).encode())
        message = connected_client_socket.recv(1024).decode()
        assert message == 'Received version'

        model = load_model("pytorch", "bla.pt")
        model = prepare_model(model)
        connected_client_socket.sendall(model)
        connected_client_socket.sendall(b'EOF')

        message = connected_client_socket.recv(1024).decode()
        assert message == 'Finished updating'
    except:
        assert False


def test_client_datachannel_start():
    global connected_client_socket, datachannel_server
    bind_datachannel_server()
    try:
        message = connected_client_socket.recv(1024).decode()
        assert message.isdecimal()

        connected_client_socket.send(b'start')
        datachannel_server.accept()
    except:
        assert False

bind_ping_server()
test_client_connect_without_id()
test_client_connect_with_id()
test_client_version()
test_client_datachannel_start()
os._exit(1)

