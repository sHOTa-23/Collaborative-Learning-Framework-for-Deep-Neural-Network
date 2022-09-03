import sys
sys.path.insert(0,"../")
from Client.app_clients import AppClient
import torch.nn as nn
import socket
import time
import threading
import yaml
import os

from Server.app_servers import AppServer

ping_socket = None
datachannel_socket = None

conf = None
with open('server_conf.yml') as f:
    conf = yaml.safe_load(f)

def score_fn(pred,golden):
    ans_index = golden.argmax(dim=1)
    score = (pred.argmax(dim=1) == ans_index).sum().item()/ans_index.shape[0]
    if score == 0:
        return 0.5
    return score

def start_server():
    app = AppServer('server_conf.yml',score_fn)
    app.run()


def test_server_datachannel_conn():
    global datachannel_socket
    datachannel_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    err = None
    time.sleep(conf['datachannel_time_interval'] + 1)
    try:
        datachannel_socket.connect((conf['ip'], conf['datachannel_port']))
    except socket.error as e:
        err = e
    assert err == None

def test_server_ping_conn():
    global ping_socket
    ping_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    err = None
    try:
        ping_socket.connect((conf['ip'], conf['ping_port']))
    except socket.error as e:
        err = e
    
    assert err == None


def test_getting_id():
    global ping_socket
    ping_socket.send(b'Give me an id you son of a bitch!')
    err = None
    try:
        message = ping_socket.recv(1024)
        assert message.decode() != ""
    except socket.error as e:
        err = e

    assert err == None

def test_connect_with_id(id, expected):
    sckt = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    
    sckt.connect((conf['ip'], conf['ping_port']))

    
    sckt.send('Connecting with id:{}'.format(id).encode())
    err = None
    try:
        message = sckt.recv(1024)
        assert message.decode() == expected
    except socket.error as e:
        err = e

    assert err == None


start_server()
test_server_ping_conn()
test_server_datachannel_conn()
test_getting_id()
id = "f4f35d119d7cd5df3f5a327c92ccc107"
test_connect_with_id(id, 'Oh I know you!')
test_connect_with_id("wrong id", 'Oh I don\'t know you!')
os._exit(1)