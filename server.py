
import socket
import threading
import numpy as np 
from io import BytesIO
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP_address = "178.62.92.57"
Port = 9000
# IP_address = "127.0.0.1"
# Port = 9000
server.bind((IP_address, Port))
server.listen(100)


def thread_handler(client_socket):
    while True:
        try:
            message = client_socket.recv(2048)
            print(message.decode())
            # send message to that client
            mss = message.decode("utf-8")+"with love"
            client_socket.send(mss.encode())
        except:
            print("Client disconnected")
            client_socket.close()
            break

def recieve(client_socket, socket_buffer_size=1024):
    buffer = BytesIO()
    while True:
        data = client_socket.recv(socket_buffer_size)
        if not data:
            break
        buffer.write(data)
        buffer.seek(-4, 2)
        if b'EOF' in buffer.read():
            client_socket.send(b'Complete')
            break
    buffer.seek(0)
    print(np.load(buffer))




while True:
    client_socket, (ip, port) = server.accept()
    print("Client connected with ip: " + ip + " and port: " + str(port))
    # t = threading.Thread(target=thread_handler, args=(client_socket,))
    # t.start()
    recieve(client_socket)
server.close()
