import socket
import threading
import logging
import os
import time
import datetime
logging.basicConfig(level=logging.NOTSET)


class PingClient():
    def __init__(self, ip, port, id_path, sleep_time):
        self.ip = ip
        self.port = port
        self.id_path = id_path
        self.sleep_time = sleep_time
        self.should_ask = True
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
    def ping_thread(self):
        while True:
            self.server.send(b'Ping')
            message = self.server.recv(1024).decode('utf-8')
            print("Should should_ask status: {}".format(self.should_ask))
            if message  == "start" and self.should_ask:
                self.should_ask = False
                logging.info("Ping Client Fired" + str(datetime.datetime.now().strftime("%H:%M:%S")))
                self.controller.fire()
                
            elif message == "start":
                logging.info("Ping Client Received start signal but is already connected")
            time.sleep(self.sleep_time)
