import socket
import threading
import secrets
import datetime
import logging
logging.basicConfig(level=logging.NOTSET)


class PingServer:
    def __init__(self, ip, port, listener_num = 100):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(listener_num)
        self.clients = {}
        t = threading.Thread(target=self.run)
        t.start()

    def run(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            print("Client connected with ip: " + ip + " and port: " + str(port))
            t = threading.Thread(target=self.client_handler, args=(client_socket,))
            t.start()


    def client_handler(self, client_socket, socket_buffer_size=1024):
        initial_message = client_socket.recv(socket_buffer_size).decode()
        if initial_message == 'Give me an id you son of a bitch!':
            client_id = secrets.token_hex(16)
            while client_id in self.clients:
                client_id = secrets.token_hex(16)
            self.clients[client_id] = datetime.datetime.now()
            client_socket.send(client_id.encode())
        else:
            client_id = initial_message[initial_message.index(':') + 1:]
            if client_id in self.clients:
                client_socket.send(b'Oh I know you!')
            else:
                client_socket.send(b'Oh I don\'t know you!')

        while True:
            data = client_socket.recv(socket_buffer_size).decode()
            current_time = datetime.datetime.now()
            print('Ping from {} at {}'.format(client_id, current_time))
            if data == "":
                print("Client {} disconnected".format(client_id))
                client_socket.close()
                break
            self.clients[client_id] = current_time
