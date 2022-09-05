import sys
sys.path.insert(0,"../")

from Client.client_controller import ClientController
from Client.ping_client import PingClient
from pydoc import cli
from this import s

from Test.test_utils import assert_equals

import socket
from Client.app_clients import AppClient
import torch.nn as nn
import time
import threading
from Server.utils import *
import os
import yaml
from Client.datachannel_client import DatachannelClient
from test_utils import *


datachannel_server = None

conf = None
with open('server_conf.yml') as f:
    conf = yaml.safe_load(f)

def bind_datachannel_server():
    global datachannel_server
    datachannel_server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    datachannel_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    datachannel_server.bind(("127.0.0.1", 9961))
    datachannel_server.listen(100)


def test_send_model():
    global datachannel_server
    client = DatachannelClient("127.0.0.1", 9961, "pytorch", "bla.pt", "input_path", "output_path", "id_path", "learning_rate", "loss_function")
    def connect(array):
        time.sleep(2)
        client.connect_server()
        client.controller = ClientController(client, PingClient("","","","","",""))
        client.send_model(array)
    threading.Thread(target=connect, args=(load_model("pytorch","bla.pt"),)).start()

    client_socket, _ = datachannel_server.accept()
    res = True
    try:
        time.sleep(2)
        client_socket.send(b'start')
        id = client_socket.recv(1024).decode()
        res = res and assert_not_equals(id, "", "Empty message received from datachannel client!!")

        client_socket.send(b'Id Verified')

        received_model = receive(client_socket, "pytorch")

        cur_model = load_model("pytorch", "bla.pt")
        cur_model = prepare_model(cur_model)

        res = res and assert_equals(cur_model, prepare_model(received_model), "Incorrect model received from datachannel client!!")

        message = client_socket.send(b'calculation completed')

    except:
        res = res and assert_false(True, "Exception occurred!!")

    return res


bind_datachannel_server()
final_score(test_send_model)
os._exit(1)