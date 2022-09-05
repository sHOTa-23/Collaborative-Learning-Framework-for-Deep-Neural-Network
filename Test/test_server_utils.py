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
from test_utils import *

tf.autograph.set_verbosity(1)
tf.get_logger().setLevel('INFO')
tensorflow_model = tf.keras.models.load_model("tf.h5") 

pytorch_model = torch.jit.load("bla.pt")


def test_prepare_model():
    res = True
    # pytorch
    res = res and assert_not_equals(prepare_model(pytorch_model), None, "Prepare model for pytorch returns None!!")
    assert prepare_model(pytorch_model) != None
    # tensorflow
    return res and assert_not_equals(prepare_model(tensorflow_model), None, "Prepare model for tensorflow returns None!!")

def test_load_model():
    res = True
    # invalid
    res = res and assert_equals(load_model("", ""), None, "load_model failed for invalid input!!")
    # pytorch
    res = res and assert_equals(load_model("pytorch", ""), None, "load_model for pytorch with empty model failed!!")
    res = res and assert_not_equals(load_model("pytorch", "bla.pt"), None, "load_model for pytorch with bla.pt failed!!")
    
    # tensorflow
    res = res and assert_equals(load_model("tensorflow", ""), None, "load_model for tensorflow with empty model failed!!")
    res = res and assert_not_equals(load_model("tensorflow", "tf.h5"), None, "load_model for tensorflow with tf.h5 failed!!")

    return res

def test_save_model():
    res = True
    # empty folder
    for f in os.listdir("saved-models"):
        os.unlink(os.path.join("saved-models", f))

    # invalid 
    save_model("invalid-type", "saved-models/bla.pt", pytorch_model)
    res = res and assert_equals(exists("saved-models/bla.pt"), False, "save_model should not work for invalid-type!!")
    # pytorch
    save_model("pytorch", "saved-models/bla.pt", pytorch_model)
    res = res and assert_equals(exists("saved-models/bla.pt"), True, "pytorch model not saved!!")
    # tensorflow
    save_model("tensorflow", "saved-models/tf.h5", tensorflow_model)
    res = res and assert_equals(exists("saved-models/tf.h5"), True, "tensorflow model not saved!!")

    # empty folder
    for f in os.listdir("saved-models"):
        os.unlink(os.path.join("saved-models", f))
    
    return res

def test_receive():
    res = True
    client = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    def connect_server():
        time.sleep(2)
        try:
            client.connect(("127.0.0.1", 9950))
        except:
            res = res and assert_false(True, "Exception occurred!!")
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
        try:
            client.send(cur_model)
            client.send(b'EOF')
        except:
            res = res and assert_false(True, "Exception occurred!!")
    threading.Thread(target=send_model, args=(cur_model,)).start()
    
    received = receive(client_socket, "pytorch")

    res = res and assert_equals(cur_model, prepare_model(received), "prepare_model failed!!")

    return res

final_score(test_prepare_model, test_load_model, test_save_model, test_receive)
os._exit(1)
# test_prepare_model()
# test_load_model()
# test_save_model()
# test_receive()
