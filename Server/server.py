
import socket
import threading
import numpy as np 
from io import BytesIO
import logging
logging.basicConfig(level=logging.NOTSET)


class Server:
    def __init__(self, ip, port,listener_num = 100):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(listener_num)
        t = threading.Thread(target=self.run)
        t.start()
        #self.run()

    def run(self):
        while True:
            client_socket, (ip, port) = self.server.accept()
            logging.debug("Client connected with ip: " + ip + " and port: " + str(port))
            # t = threading.Thread(target=thread_handler, args=(client_socket,))
            # t.start()
            self.recieve(client_socket)

    def recieve(self,client_socket, socket_buffer_size=1024):
        buffer = BytesIO()
        while True:
            data = client_socket.recv(socket_buffer_size)
            if not data:
                break
            buffer.write(data)
            buffer.seek(-4, 2)
            if b'EOF' in buffer.read():
                client_socket.send(b'Done')
                break
        buffer.seek(0)
        logging.info(np.load(buffer))
        logging.info("Received")


    def thread_handler(client_socket):
        while True:
            try:
                message = client_socket.recv(2048)
                logging.info(message.decode())
                # send message to that client
                mss = message.decode("utf-8")+" is love"
                client_socket.send(mss.encode())
            except:
                logging.debug("Client disconnected")
                client_socket.close()
                break






# while True:
#     client_socket, (ip, port) = server.accept()
#     print("Client connected with ip: " + ip + " and port: " + str(port))
#     # t = threading.Thread(target=thread_handler, args=(client_socket,))
#     # t.start()
#     recieve(client_socket)
# server.close()
