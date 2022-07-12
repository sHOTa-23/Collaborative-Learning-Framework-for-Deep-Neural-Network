import socket
import threading
import logging
import datetime
from Core.utils import prepare_model,receive
from Core.ClientsRepository import ClientsRepository
logging.basicConfig(level=logging.NOTSET)


class DatachannelServer:
    def __init__(self, ip, port,mongodb_host, listener_num = 100, gap_time=10):
        self.ip = ip
        self.port = port
        self.listener_num = listener_num
        self.gap_time = gap_time
        
        self.clientsDB = ClientsRepository(mongodb_host)
        
    
    def start(self):
        self.last_time = datetime.datetime.now()
        self.barrier = threading.Barrier(2)
        self.received_values = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.listener_num)
        # t = threading.Thread(target=self.run)
        # t.start()
        self.run()

    def run(self):
        counter_thread = threading.Thread(target=self.count_average)
        counter_thread.start()
        time_controller_thread = threading.Thread(target=self.check_time)
        time_controller_thread.start()
        main_thread = threading.Thread(target=self.runner_thread)
        main_thread.start()


    

   
    def count_average(self):
        try:
            self.barrier.wait()
        except:
            pass
        for client_socket in self.received_values:
            data = prepare_model(self.received_values[client_socket])
            client_socket.sendall(data)
            client_socket.sendall(b'EOF')
        
        # Interrupt server.accept() with fake connection
        fake_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_address = self.ip
        Port = self.port
        fake_server.connect((IP_address, Port))

    def check_time(self):
        while True:
            current_time = datetime.datetime.now()
            dif = current_time - self.last_time
            dif = dif.total_seconds()
            if dif > self.gap_time:
                self.barrier.abort()
                break

    def client_handler(self, client_socket):
        client = client_socket.recv(1024).decode()
        if self.barrier.broken:
            client_socket.send(b'I won\'t receive connections anymore!')
            return
        model = receive(client_socket)
        if client not in self.clientsDB.get_clients():
            client_socket.send(b'I don\'t know you!')
            return
        self.last_time = datetime.datetime.now()
        self.received_values[client_socket] = model

    def runner_thread(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            if self.barrier.broken:
                break
            logging.info('Client connected on datachannel server from {}:{}'.format(ip, port))
            t = threading.Thread(target=self.client_handler, args=(client_socket,))
            t.start()

        self.server.close()
