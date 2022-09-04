import socket
import threading
import secrets
import datetime
import logging
import time
from Server.utils import prepare_model,load_model
logging.basicConfig(level=logging.NOTSET)


class PingServer:
    def __init__(self, ip, port,clientsDB,server_model_path,model_type,time_interval,starting_time = datetime.datetime.now(), listener_num = 100):
        self.ip = ip
        self.port = port
        self.clientsDB = clientsDB
        self.server_model_path = server_model_path
        self.model_type = model_type
        self.starting_time = starting_time
        self.time_interval = time_interval
        self.listener_num = listener_num
        logging.debug("Ping Server initialized")
        
        
    def start(self,controller):
        self.controller = controller
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.listener_num)
        logging.debug("Ping Server Has been started on {}:{}".format(self.ip, self.port))
        t = threading.Thread(target=self.run)
        t.start()
        t1 = threading.Thread(target=self.time_checker)
        self.is_time = False
        self.is_legal_to_send = True
        t1.start()

    def run(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            logging.info("Client {} connected on ping server from {}".format(client_socket, ip))
            t = threading.Thread(target=self.client_handler, args=(client_socket,))
            t.start()

    def time_checker(self):
        while True:
            current_time = datetime.datetime.now()
            time_diff = current_time - self.starting_time
            if time_diff.seconds > self.time_interval:
                logging.debug("Datachanel Server Start Fire Called")
                self.is_legal_to_send = False
                self.controller.fire()
                self.starting_time = current_time
                self.is_time = True
            else:
                self.is_time = False
            time.sleep(1)

    def client_handler(self, client_socket, socket_buffer_size=1024):
        initial_message = client_socket.recv(socket_buffer_size).decode()
        logging.debug("Message has been received to Ping Server")
        
        clients = self.clientsDB.get_clients()
        if initial_message == 'Give me an id you son of a bitch!':
            client_id = secrets.token_hex(16)
            while client_id in clients:
                client_id = secrets.token_hex(16)
            self.clientsDB.add_client(client_id)
            client_socket.send(client_id.encode())
            logging.debug("ID has been sent to new Client")
        elif initial_message == '':
            return
        else:
            client_id = initial_message[initial_message.index(':') + 1:]
            if client_id in clients:
                client_socket.send(b'Oh I know you!')
            else:
               client_socket.send(b'Oh I don\'t know you!')
               client_socket.close()
               return


        while True:
            data = client_socket.recv(socket_buffer_size).decode()
            current_time = datetime.datetime.now()
            logging.info('Ping from {} at {}, message: {}'.format(client_id, current_time, data))
            if data == "":
                logging.debug("Client {} disconnected".format(client_id))
                client_socket.close()
                break
            client_version = int(data)
            logging.info('Version of the client\'s model is {}'.format(client_version))
            if client_version < self.controller.get_version():
                self.controller.version_updating.acquire()
                client_socket.send(b'update')
                print(client_socket.recv(1024).decode())
                client_socket.send(str(self.controller.get_version()).encode())
                print(client_socket.recv(1024).decode())
                model_path = self.server_model_path + 'model_' + str(self.controller.get_version()) + '.pt'
                model = load_model(self.model_type,model_path)
                data = prepare_model(model)
                client_socket.sendall(data)
                client_socket.sendall(b'EOF')
                logging.info("Averaged Model Sent to {}".format(client_socket.getpeername()))
                print(client_socket.recv(1024).decode())
                self.controller.version_updating.release()
            elif self.is_time:
                client_socket.send(b'start')
                logging.debug("Sent start signal to the client: {}".format(client_socket.getpeername()))
            else:
                client_socket.send(b'not start')
            