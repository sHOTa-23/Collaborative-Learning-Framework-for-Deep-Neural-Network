import socket
import threading
from io import BytesIO
import logging
import pickle
logging.basicConfig(level=logging.NOTSET)

# from t1 import Net
# net = Net()
# from tensorflow import keras
# from tensorflow.keras import layers
# num_classes = 10
# input_shape = (28, 28, 1)
# model = keras.Sequential(
#     [
#         keras.Input(shape=input_shape),
#         layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
#         layers.MaxPooling2D(pool_size=(2, 2)),
#         layers.Flatten(),
#         layers.Dropout(0.5),
#         layers.Dense(num_classes, activation="softmax"),
#     ]
# )

class DatachannelClient():
    def __init__(self, ip, port,model_type,model_path,input_path,output_path,learning_rate,loss_function):
        self.ip = ip
        self.port = port
        self.model_type = model_type
        self.model_path = model_path
        self.learning_rate = learning_rate
        self.input_path = input_path
        self.output_path = output_path
        self.loss_function = loss_function
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.load_model()
        self.load_input()
        self.calculate_new_waits()
        self.test_sending()

    def calculate_new_waits(self):
        if self.model_type == "pytorch":
            out = self.model(self.input)
            import torch.nn as nn
            import torch
           # MSE_loss_fn = nn.MSELoss()
            loss = self.loss_function(out, self.output)
            loss.backward()
            logging.info("Gradients calculated")
            with torch.no_grad():
                for param in self.model.parameters():
                    param -= param.grad * self.learning_rate
            
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
            print(self.model.state_dict().items())
            print(self.model.conv1.weight[0, 0])
        logging.info("Model loaded")
   
    @staticmethod
    def prepare_model(model):
        buffer = BytesIO()
        logging.info(str(type(model).__bases__))
        model_type = str(type(model))
        model_parent_type = str(type(model).__bases__)
        if 'keras' in model_type or 'keras' in model_parent_type:
            import tensorflow as tf
            tf.get_logger().setLevel(logging.ERROR)
            from tensorflow.keras.models import save_model
            import h5py
            with h5py.File(buffer, 'w') as f:
                save_model(model, f, include_optimizer=True)
        elif 'sklearn' in model_type or 'sklearn' in model_parent_type:
            from joblib import load, dump
            dump(model, buffer)
        elif 'torch' in model_type or 'torch' in model_parent_type:
            import torch
            scripted_model = torch.jit.script(model)
            torch.jit.save(scripted_model, buffer)
        buffer.seek(0)
        return buffer.read()

    def send_model(self,array):
        data = DatachannelClient.prepare_model(array)
        self.server.sendall(data)
        self.server.sendall(b'EOF')
        logging.info("Sent")
        self.server.recv(1024)

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
