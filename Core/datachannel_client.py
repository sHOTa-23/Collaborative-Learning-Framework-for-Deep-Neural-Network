import socket
import threading
from io import BytesIO
import logging
import pickle
from Core.utils import prepare_model,receive,load_data

logging.basicConfig(level=logging.NOTSET)


class DatachannelClient():
    def __init__(self, ip, port,model_type,model_path,input_path,output_path,learning_rate,loss_function,optimizer = None):
        self.ip = ip
        self.port = port
        self.model_type = model_type
        self.model_path = model_path
        self.learning_rate = learning_rate
        self.input_path = input_path
        self.output_path = output_path
        self.loss_function = loss_function
        self.optimizer = optimizer

    def start(self):
        with open('id.txt') as f:
            self.id = f.read()
        f.close()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.load_model()
        self.load_input()
        self.calculate_new_waits()
        self.send_model(self.model)
        

    def calculate_new_waits(self):
        if self.model_type == "pytorch":
            out = self.model(self.input)
            import torch
           # MSE_loss_fn = nn.MSELoss()
            loss = self.loss_function(out, self.output)
            loss.backward()
            logging.info("Gradients calculated")
            with torch.no_grad():
                for param in self.model.parameters():
                    param -= param.grad * self.learning_rate
            
        elif self.model_type == "tensorflow":
            import tensorflow as tf
            
            logging.info("Gradients calculated")
            with tf.GradientTape() as tape:
    # Trainable variables are automatically tracked by GradientTape
                current_loss = self.loss_function(self.output,self.model(self.input))
            gradient = tape.gradient(current_loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(gradient, self.model.trainable_variables))
                # for param in self.model.trainable_variables:
                #     param -= param.grad * self.learning_rate
        logging.info("Weights updated")

    def load_input(self):
        self.input = pickle.load(open(self.input_path, 'rb'))
        self.output = pickle.load(open(self.output_path, 'rb'))
        logging.info("Input loaded")

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
        logging.info("Model loaded")
        
   

    def send_model(self,array):
        data = prepare_model(array)
        self.server.sendall(self.id.encode())
        self.server.sendall(data)
        self.server.sendall(b'EOF')
        model = receive(self.server)

    def reading_thread(self):
        while True:
            try:
                message = self.server.recv(2048)
                if message.decode() == "":
                    logging.debug("Server disconnected")
                    self.server.close()
                logging.info(message.decode('utf-8'))
            except:
                logging.debug("Server disconnected")
                self.server.close()
                break
    
    def writing_thread(self):
        while True:
            try:
                message = input()
                self.server.send(message.encode())
            except:
                logging.debug("Server disconnected")
                self.server.close()

    def test_sending(self):
        # array = np.random.rand(30,30,30)
        self.send_model(self.model)
        self.server.close()
