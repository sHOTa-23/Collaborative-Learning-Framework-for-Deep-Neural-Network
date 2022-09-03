from http import server
import sys
sys.path.insert(0,"../")
import socket
import yaml
import os
from Server.app_servers import AppServer
from Server.utils import *
import time

sckt = None
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


def test_lower_version():
    global sckt
    sckt = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    
    sckt.connect((conf['ip'], conf['ping_port']))

    sckt.send('Connecting with id:{}'.format("f4f35d119d7cd5df3f5a327c92ccc107").encode())
    message = sckt.recv(1024)
    assert message.decode() == "Oh I know you!"

    sckt.send('0'.encode())
    err = None

    try:
        message = sckt.recv(1024).decode()
        assert message == 'update'

        sckt.send(b'Send version and model')
        message = sckt.recv(1024).decode()
        assert int(message) > 0 

        sckt.send(b'Received version')
        received = receive(sckt, conf['model_type'])
        
        cur_model = load_model("pytorch", "../Example/models/server/model_8.pt")
        cur_model = prepare_model(cur_model)

        assert cur_model == prepare_model(received)

        sckt.send(b'Finished updating')

    except socket.error as e:
        err = e
    
    assert err == None


def test_higher_version():
    global sckt
    sckt.send(b'10')
    err = None
    try:
        message = sckt.recv(1024).decode()
        assert message != 'update'
    except socket.error as e:
        err = e 
    
    assert err == None



start_server()
test_lower_version()
test_higher_version()
os._exit(1)