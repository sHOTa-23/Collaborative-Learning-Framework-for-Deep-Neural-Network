import socket
import threading
from io import BytesIO
import logging
import pickle
from Core.utils import prepare_model,receive

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
        logging.debug("Datachannel client initialized")

    def start(self):
        with open(self.id_path) as f:
            self.id = f.read()
        f.close()
        self.connect_server()
        self.load_model()
        self.load_input()
        self.calculate_new_waits()
        self.send_model(self.model)
        
    def connect_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        logging.debug("Connected to server")

    def calculate_new_waits(self):
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
        logging.info("Input and Output Loaded")

    def load_model(self):
        if self.model_type == "sklearn":
            from joblib import load
            self.model = load(self.model_path)
        elif self.model_type == "tensorflow":
            import tensorflow as tf
            tf.get_logger().setLevel(logging.ERROR)
            from tensorflow.keras.models import load_model
            self.model = load_model(self.model_path)
        elif self.model_type == "pytorch":
            import torch
            self.model = torch.jit.load(self.model_path)
        logging.info(f"{self.model_type} Model loaded")     

    def send_model(self,array):
        data = prepare_model(array)
        self.server.sendall(self.id.encode())
        self.server.sendall(data)
        self.server.sendall(b'EOF')
        logging.info("Model sent by Client")
        model = receive(self.server)
        logging.info("Model Received by Client")