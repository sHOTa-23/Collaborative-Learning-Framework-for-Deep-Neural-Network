from http import server
import sys
sys.path.insert(0,"../")

from Test.test_utils import *
import socket
import yaml
import os
from Server.app_servers import AppServer
from Server.utils import *
import time
from Client.app_clients import AppClient
import torch.nn as nn

sckt = None
version = '0'

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

def start_client():
    loss = nn.MSELoss()
    app = AppClient('id_test/client_conf.yml',loss)
    app.run()


def test_lower_version():
    res = True
    global sckt,version
    sckt = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    
    sckt.connect((conf['ip'], conf['ping_port']))

    sckt.send('Connecting with id:{}'.format("f4f35d119d7cd5df3f5a327c92ccc107").encode())
    message = sckt.recv(1024)

    res = res and assert_equals(message.decode(), "Oh I know you!", "Ping server could not recognise correct id!!")

    sckt.send('0'.encode())
    err = None

    try:
        message = sckt.recv(1024).decode()
        res = res and assert_equals(message, 'update', "Incorrect message received from ping server")

        sckt.send(b'Send version and model')
        version = sckt.recv(1024).decode()
        res = res and assert_higher(int(version), 0, "version should be higher than 0") 

        sckt.send(b'Received version')
        received = receive(sckt, conf['model_type'])
        
        cur_model = load_model("pytorch", "models/server/model_{}.pt".format(version))
        cur_model = prepare_model(cur_model)

        res = res and assert_equals(cur_model, prepare_model(received), "Incorrect model received from ping server!!")

        sckt.send(b'Finished updating')

    except socket.error as e:
        err = e
    
    return assert_equals(err, None, "Exception occurred!!")


def test_higher_version():
    global sckt
    sckt.send(b'100000000')
    err = None
    res = True
    try:
        message = sckt.recv(1024).decode()
        res = res and assert_not_equals(message, 'update', "Incorrect message received from ping server!!")
        # assert message != 'update'
    except socket.error as e:
        err = e 
    

    return res and assert_equals(err, None, "Exception occurred!!")


def test_version_update():
    global sckt, version
    start_client()
    res = True
    time.sleep((conf['datachannel_time_interval'] + conf['datachannel_gap_time']) * 7)

    sckt.send(version.encode())

    err = None
    try:
        message = sckt.recv(1024).decode()
        res = res and assert_equals(message, 'update', "Incorrect message received from ping server!!")
    except socket.error as e:
        err = e
    
    return res and assert_equals(err, None, "Exception occurred!!")





start_server()
final_score(test_lower_version, test_higher_version, test_version_update)

# test_lower_version()
# test_higher_version()
# test_version_update()
os._exit(1)