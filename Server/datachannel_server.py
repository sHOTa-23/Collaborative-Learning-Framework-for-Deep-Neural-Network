import socket
import threading
import numpy as np 
import torch
from io import BytesIO
import logging
logging.basicConfig(level=logging.NOTSET)


class DatachannelServer:
    def __init__(self, ip, port, listener_num = 100):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(listener_num)
        t = threading.Thread(target=self.run)
        t.start()

    def run(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            logging.debug("Client connected with ip: " + ip + " and port: " + str(port))
            self.receive(client_socket)

    def receive(self,client_socket, socket_buffer_size=1024):
        buffer = BytesIO()
        while True:
            data = client_socket.recv(socket_buffer_size)
            if not data:
                break
            buffer.write(data)
            buffer.seek(-4, 2)
            if b'EOF' in buffer.read():
                client_socket.send(b'Done')
                break
        buffer.seek(0)
        model = DatachannelServer.load_data(buffer)
        logging.info(model)
        logging.info("Received")
    
    @staticmethod
    def load_data(file: BytesIO):
        data = file.read()[:-3]
        file.seek(0)
        if b'sklearn' in data:
            from joblib import load, dump
            return load(file)
        elif b'HDF' in data:
            import tensorflow as tf
            tf.get_logger().setLevel(logging.ERROR)
            from tensorflow.keras.models import load_model
            import h5py
            with h5py.File(file, 'r') as f:
                model = load_model(f)
                print(model.summary())
                print(print(model.trainable_variables)) 
            return model
        else:
            model = torch.jit.load(file)
            print(model.conv1.weight[0, 0])
            return model


    def thread_handler(client_socket):
        while True:
            try:
                message = client_socket.recv(2048)
                logging.info(message.decode())
                # send message to that client
                mss = message.decode("utf-8")+" is love"
                client_socket.send(mss.encode())
            except:
                logging.debug("Client disconnected")
                client_socket.close()
                break
