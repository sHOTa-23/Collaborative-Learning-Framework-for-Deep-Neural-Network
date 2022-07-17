import socket
import threading
import logging
import os
import time
import datetime
from Client.utils import receive,save_model
logging.basicConfig(level=logging.NOTSET)


class PingClient():
    def __init__(self, ip, port, id_path, model_path,model_type, sleep_time):
        self.ip = ip
        self.port = port
        self.id_path = id_path
        self.model_path = model_path
        self.model_type = model_type
        self.sleep_time = sleep_time
        self.should_ask = True
        self.updating = False
        logging.debug('Ping Client Initialized')

    def start(self,controller):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        logging.debug('Ping Client Connected to server')
        self.controller = controller
        self.run()

    def run(self):
        self.auth()
        t = threading.Thread(target=self.ping_thread)
        t.start()

    def auth(self):
        if not os.path.exists(self.id_path):
            new_id = self.get_id_from_server()
            logging.debug('Ping Client Got id from server:{}'.format(new_id))
            with open(self.id_path, 'x') as f:
                f.write(new_id)
        else:
            with open(self.id_path) as f:
                id = f.read()
                self.connect_server_with_id(id)
        f.close()
        logging.debug('Ping Client Authenticated')

    def get_id_from_server(self):
        try:
            self.server.send(b'Give me an id you son of a bitch!')
        except:
            logging.warning("In get_id_from_server, exception raised while sending")
            self.server.close()
            exit()

        try:
            message = self.server.recv(1024)
            if message.decode() == "":
                logging.debug("empty message has been received")
                self.server.close()
                exit()
            return message.decode('utf-8')
        except:
            logging.warning("In get_id_from_server, exception raised while receiving")
            self.server.close()
            exit()

    def connect_server_with_id(self, id):
        try:
            self.server.send('Connecting with id:{}'.format(id).encode())
        except:
            logging.warning("In connect_server_with_id, exception raised while sending")
            self.server.close()
            exit()
        try:
            message = self.server.recv(1024)
            if message.decode() == "":
                logging.debug("empty message has been received")
                self.server.close()
                exit()
        except:
            logging.warning("In connect_server_with_id, exception raised while receiving")
            self.server.close()
            exit()

    def change_status(self):
        self.should_ask = True
    
    def get_status(self):
        return self.should_ask

    def change_updating_status(self):
        self.updating = False

    def get_updating_status(self):
        return self.updating

    def ping_thread(self):
        while True:
            self.server.send(str(self.controller.get_version()).encode())
            message = self.server.recv(1024).decode('utf-8')
            print("Should should_ask status: {}".format(self.should_ask))
            if message  == "start" and self.should_ask:
                self.should_ask = False
                logging.info("Ping Client Fired " + str(datetime.datetime.now().strftime("%H:%M:%S")))
                self.controller.fire()
            elif message == "start":
                logging.info("Ping Client Received start signal but is already connected")
            elif message == "update" and not self.updating:
                self.updating = True
                logging.info("Started updating model at " + str(datetime.datetime.now().strftime("%H:%M:%S")))
                self.controller.updating_lock.acquire()
                self.update_model()
                self.controller.updating_lock.release()
            elif message == "update":
                logging.info("Updating model not done yet")
            time.sleep(self.sleep_time)

    def update_model(self):
        self.server.send(b'Send version and model')
        new_version = int(self.server.recv(1024).decode())
        self.server.send(b'Received version')
        new_model = receive(self.server,self.model_type)
        print(self.model_path)
        save_model(self.model_type,self.model_path,new_model)
        logging.info("Model updated to version {}".format(new_version))
        self.server.send(b'Finished updating')
        self.controller.set_version(new_version)
        self.change_updating_status()