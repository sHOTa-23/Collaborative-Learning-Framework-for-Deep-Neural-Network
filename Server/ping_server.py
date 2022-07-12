import socket
import threading
import secrets
import datetime
import logging
from Core.ClientsRepository import ClientsRepository
logging.basicConfig(level=logging.NOTSET)


class PingServer:
    def __init__(self, ip, port,mongodb_host,starting_time = datetime.datetime.now(),time_interval = 6, listener_num = 100):
        self.ip = ip
        self.port = port
        self.mongodb_host = mongodb_host
        self.starting_time = starting_time
        self.time_interval = time_interval
        self.listener_num = listener_num
        
    def start(self,controller):
        self.controller = controller
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.listener_num)
        self.clientsDB = ClientsRepository(self.mongodb_host)
        t = threading.Thread(target=self.run)
        t.start()

    def run(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            logging.info("Client {} connected on ping server from {}".format(client_socket, ip))
            t = threading.Thread(target=self.client_handler, args=(client_socket,))
            t.start()


    def client_handler(self, client_socket, socket_buffer_size=1024):
        initial_message = client_socket.recv(socket_buffer_size).decode()
        clients = self.clientsDB.get_clients()
        if initial_message == 'Give me an id you son of a bitch!':
            client_id = secrets.token_hex(16)
            while client_id in clients:
                client_id = secrets.token_hex(16)
            self.clientsDB.add_client(client_id)
            client_socket.send(client_id.encode())
        else:
            client_id = initial_message[initial_message.index(':') + 1:]
            if client_id in clients:
                client_socket.send(b'Oh I know you!')
            else:
               client_socket.send(b'Oh I don\'t know you!')

        while True:
            data = client_socket.recv(socket_buffer_size).decode()
            current_time = datetime.datetime.now()
            logging.info('Ping from {} at {}'.format(client_id, current_time))
            if data == "":
                logging.debug("Client {} disconnected".format(client_id))
                client_socket.close()
                break
            time_diff = current_time - self.starting_time
            if time_diff.seconds > self.time_interval:
                self.controller.fire()
                self.starting_time = current_time
                client_socket.send(b'start')

            else:
                client_socket.send(b'not start')

            self.clientsDB.add_client(client_id)
