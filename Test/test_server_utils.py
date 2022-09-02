import sys
sys.path.insert(0,"../")
from Server.utils import *
import torch
import tensorflow as tf
from os.path import exists
import os
import time
import socket
import threading

tf.autograph.set_verbosity(1)
tf.get_logger().setLevel('INFO')
tensorflow_model = tf.keras.models.load_model("tf.h5") 

pytorch_model = torch.jit.load("bla.pt")


def test_prepare_model():
    # pytorch
    assert prepare_model(pytorch_model) != None
    # tensorflow
    assert prepare_model(tensorflow_model) != None

def test_load_model():
    # invalid
    assert load_model("", "") == None
    # pytorch
    assert load_model("pytorch", "") == None
    assert load_model("pytorch", "bla.pt") != None
    # tensorflow
    assert load_model("tensorflow", "") == None
    assert load_model("tensorflow", "tf.h5") != None

def test_save_model():
    # empty folder
    for f in os.listdir("saved-models"):
        os.unlink(os.path.join("saved-models", f))

    # invalid 
    save_model("invalid-type", "saved-models/bla.pt", pytorch_model)
    assert exists("saved-models/bla.pt") == False
    # pytorch
    save_model("pytorch", "saved-models/bla.pt", pytorch_model)
    assert exists("saved-models/bla.pt") == True
    # tensorflow
    save_model("tensorflow", "saved-models/tf.h5", tensorflow_model)
    assert exists("saved-models/tf.h5") == True

    # empty folder
    for f in os.listdir("saved-models"):
        os.unlink(os.path.join("saved-models", f))

def test_receive():
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    def connect_server():
        time.sleep(2)
        client.connect(("127.0.0.1", 9950))
    threading.Thread(target=connect_server).start()
    
    server = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 9950))
    server.listen(100)
    client_socket, (ip, port) = server.accept()

    cur_model = load_model("pytorch", "bla.pt")
    cur_model = prepare_model(cur_model)

    def send_model(cur_model):
        time.sleep(2)
        client.send(cur_model)
        client.send(b'EOF')
    threading.Thread(target=send_model, args=(cur_model,)).start()
    
    received = receive(client_socket, "pytorch")

    assert cur_model == prepare_model(received)


test_prepare_model()
test_load_model()
test_save_model()
test_receive()
