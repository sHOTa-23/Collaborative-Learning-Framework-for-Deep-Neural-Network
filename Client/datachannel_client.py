import socket
import threading
from io import BytesIO
import logging
import pickle
import os
from Client.utils import prepare_model,load_model

logging.basicConfig(level=logging.NOTSET)


class DatachannelClient():
    def __init__(self, ip, port,model_type,model_path,input_path,output_path,id_path,learning_rate,loss_function,optimizer = None):
        self.ip = ip
        self.port = port
        self.model_type = model_type
        self.model_path = model_path
        self.learning_rate = learning_rate
        self.input_path = input_path
        self.output_path = output_path
        self.id_path = id_path
        self.loss_function = loss_function
        self.optimizer = optimizer
        self.id = "empty"
        logging.debug("Datachannel client initialized")

    def start(self, controller):
        logging.debug("Datachannel client started")
        with open(self.id_path) as f:
            self.id = f.read()
        f.close()
        self.controller = controller
        self.connect_server()
        self.controller.updating_lock.acquire()
        self.model = load_model(self.model_type,self.model_path)
        self.load_input()
        self.calculate_new_weights()
        self.send_model(self.model)
        self.controller.updating_lock.release()
        
    def connect_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        logging.debug("Connected to server from {}".format(self.server.getsockname()))
        # Waiting for server to get permission to continue

    def calculate_new_weights(self):
        if self.model_type == "pytorch":
            out = self.model(self.input)
            import torch
            loss = self.loss_function(out, self.output)
            loss.backward()
            logging.debug(f"{self.model_type} Gradients calculated")
            with torch.no_grad():
                for param in self.model.parameters():
                    param -= param.grad * self.learning_rate   
        elif self.model_type == "tensorflow":
            import tensorflow as tf
            logging.debug(f"{self.model_type} Gradients calculated")
            with tf.GradientTape() as tape:
                current_loss = self.loss_function(self.output,self.model(self.input))
            gradient = tape.gradient(current_loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(gradient, self.model.trainable_variables))
        logging.debug(f"{self.model_type} Weights updated")

    def load_input(self):
        self.input = pickle.load(open(self.input_path, 'rb'))
        self.output = pickle.load(open(self.output_path, 'rb'))
        # os.remove(self.input_path)
        # os.remove(self.output_path)
        logging.info("Input and Output Loaded")

       

    def set_controller(self,controller):
        self.controller = controller
    

    def send_model(self,array):
        message = self.server.recv(1024).decode()
        if message == 'start':
            logging.debug("Server ready to receive model")
        else :
            logging.debug("Server did not receive start message instead received: " + message)
        
        logging.info('client Sent ID: {}'.format(self.id))
        self.server.sendall(self.id.encode())
        status = self.server.recv(1024).decode()
        if status == 'Id Verified':
            logging.debug("Server received ID")
        data = prepare_model(array)
       
        self.server.sendall(data)
        self.server.sendall(b'EOF')
        logging.info("Model sent by Client")
        message = self.server.recv(1024).decode()
        if message == 'calculation completed':
            logging.debug("Server ready to receive new model")
            logging.info(str(self.controller.ping_client.get_status()) + " Before")
            self.controller.fire_ping()
            logging.info(str(self.controller.ping_client.get_status()) + " After")
        else:
            logging.debug("Server did not receive calculation completed message instead received: " + message)
            self.controller.fire_ping()
