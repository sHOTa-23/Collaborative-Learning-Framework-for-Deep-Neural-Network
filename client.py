# Python program to implement client side of chat room.
import socket
import threading
import numpy as np
from io import BytesIO
import pickle
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = "178.62.92.57"
Port = 9000
# IP_address = "127.0.0.1"
# Port = 9000
server.connect((IP_address, Port))



def prepare_numpy_array(array):
    buffer = BytesIO()
    np.save(buffer, array, allow_pickle=True)
    buffer.seek(0)
    return buffer.read()

def send_array(array):
    data = prepare_numpy_array(array)
    server.sendall(data)
    server.sendall(b'EOF')
    server.recv(1024)



# def reading_thread():
#     while True:
#         try:
#             message = server.recv(2048)
#             if message.decode() == "":
#                 print("Server disconnected")
#                 server.close()
#             print(message.decode('utf-8'))
#         except:
#             print("Server disconnected")
#             server.close()
#             break
    
# reader_thread = threading.Thread(target=reading_thread)
# reader_thread.start()

# def writing_thread():
#     while True:
#         try:
#             message = input()
#             server.send(message.encode())
#         except:
#             print("Server disconnected")
#             server.close()
#             exit()

# writing_thread = threading.Thread(target=writing_thread)
# writing_thread.start()

array = np.random.rand(10,10,10)
print("sending" + str(array))
send_array(array)