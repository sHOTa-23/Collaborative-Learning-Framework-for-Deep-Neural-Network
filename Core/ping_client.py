import socket
import threading
import logging
import os
import time
logging.basicConfig(level=logging.NOTSET)


class PingClient():
    def __init__(self, ip, port, id_path, sleep_time):
        self.ip = ip
        self.port = port
        self.id_path = id_path
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.sleep_time = sleep_time
        self.run()

    def run(self):
        self.auth()
        t = threading.Thread(target=self.ping_thread)
        t.start()

    def auth(self):
        if not os.path.exists(self.id_path):
            new_id = self.getIdFromServer()
            print('Got id from server:{}'.format(new_id))
            with open(self.id_path, 'x') as f:
                f.write(new_id)
        else:
            with open(self.id_path) as f:
                id = f.read()
                print('My id is', id)
                self.connectServerWithId(id)
        f.close()

    def getIdFromServer(self):
        # Ping server to get an id
        try:
            self.server.send(b'Give me an id you son of a bitch!')
        except:
            print("Server disconnected")
            self.server.close()
            exit()

        # Get id from server and close in case of failure
        try:
            message = self.server.recv(1024)
            if message.decode() == "":
                print("Server disconnected")
                self.server.close()
                exit()
            return message.decode('utf-8')
        except:
            print("Server disconnected")
            self.server.close()
            exit()

    def connectServerWithId(self, id):
        # Connect server with id
        try:
            self.server.send('Connecting with id:{}'.format(id).encode())
        except:
            print("Server disconnected")
            self.server.close()
            exit()

        # Accept connection from server
        try:
            message = self.server.recv(1024)
            if message.decode() == "":
                print("Server disconnected")
                self.server.close()
                exit()
            print(message.decode('utf-8'))
        except:
            print("Server disconnected")
            self.server.close()
            exit()

    def ping_thread(self):
        while True:
            self.server.send(b'Ping')
            time.sleep(self.sleep_time)
