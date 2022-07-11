import socket
import threading
import numpy as np
from io import BytesIO
import logging
logging.basicConfig(level=logging.NOTSET)


class Client():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.ip, self.port))
        self.test_sending()

    @staticmethod
    def prepare_numpy_array(array):
        buffer = BytesIO()
        np.save(buffer, array, allow_pickle=True)
        buffer.seek(0)
        return buffer.read()

    def send_numpy(self,array):
        data = Client.prepare_numpy_array(array)
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
        array = np.random.rand(30,30,30)
        self.send_numpy(array)
        self.server.close()
    
# reader_thread = threading.Thread(target=reading_thread)
# reader_thread.start()



# writing_thread = threading.Thread(target=writing_thread)
# writing_thread.start()
