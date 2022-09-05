import socket
import threading
import logging
import datetime
import os


from Server.utils import prepare_model,receive,save_model,load_input
logging.basicConfig(level=logging.NOTSET)


class DatachannelServer:
    def __init__(self, ip, port,clientsDB,server_model_path,model_type,golden_data_input,golden_data_output,score_fn,gap_time=20, listener_num = 100):
        self.ip = ip
        self.port = port
        self.server_model_path = server_model_path
        self.model_type = model_type
        self.listener_num = listener_num
        self.gap_time = gap_time
        self.clientsDB = clientsDB
        self.server = None
        self.golden_data_input,self.golden_data_output = load_input(golden_data_input,golden_data_output)
        self.score_fn = score_fn
        self.received_values = {}
        logging.debug('Datachannel initialized')
    
        
    def start(self, server_controller):
        if self.server is not None and self.server.fileno() != -1:
            logging.info("Datachannel server is already running")
            return
        self.server_controller = server_controller
        self.last_time = None
        self.barrier = threading.Barrier(2)
        self.received_values = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(self.listener_num)
        logging.debug('Datachannel server started on {}:{}'.format(self.ip, self.port))
        self.run()

    def run(self):
        counter_thread = threading.Thread(target=self.count_average)
        counter_thread.start()
        logging.debug('counter_thread started')
        time_controller_thread = threading.Thread(target=self.check_time)
        time_controller_thread.start()
        logging.debug('time_controller_thread started')
        main_thread = threading.Thread(target=self.runner_thread)
        main_thread.start()
        logging.debug('main_thread started')

    
    def calculate_average(self):
        if self.model_type == "pytorch":
            import torch
            keys = list(self.received_values.keys())
            print("SDASDASDASDASD",self.received_values)
            if len(keys) == 0:
                return None
            init_weights = self.received_values[keys[0]]
            averaging_weight = self.score_fn(init_weights(self.golden_data_input),self.golden_data_output)
            sum_weighted_average = averaging_weight
            with torch.no_grad():
                for i in init_weights.parameters():
                    i*=averaging_weight
            print("Before")
            for key in keys:
                for i in self.received_values[key].parameters():
                    print(i)
                print("Another Model")
            for mdl in range(1,len(keys)):
                averaging_weight = self.score_fn(self.received_values[keys[mdl]](self.golden_data_input),self.golden_data_output)
                sum_weighted_average += averaging_weight
                with torch.no_grad():
                    for (i,j) in zip(init_weights.parameters(),self.received_values[keys[mdl]].parameters()):
                        i+=averaging_weight*j 
            
            with torch.no_grad():
                for i in init_weights.parameters():
                    i/=sum_weighted_average
            
            print("After")
            for i in init_weights.parameters():
                print(i)
            
            return init_weights
        elif self.model_type == "tensorflow":
            models = list(self.received_values.values())
            if len(models) == 0:
                print("AAABa")
                return None
            import tensorflow as tf
            print("Before")
            for model in models:
                for layer in model.layers:
                    print(layer.get_weights())
                    print("\n")
            model = models[0]
            averaging_weight = self.score_fn(model(self.golden_data_input),self.golden_data_output)
            sum_weighted_average = averaging_weight
            for layer in model.layers:
                curr_weights = layer.get_weights()
                for i in range(len(curr_weights)):
                    curr_weights[i] = curr_weights[i] * averaging_weight
                layer.set_weights(curr_weights)
            for model in models[1:]:
                averaging_weight = self.score_fn(model(self.golden_data_input),self.golden_data_output)
                sum_weighted_average += averaging_weight
                for (layer0,layer1) in zip(models[0].layers,model.layers):
                    curr_weights = layer0.get_weights()
                    weights = layer1.get_weights()
                    for i in range(len(curr_weights)):
                        curr_weights[i] = curr_weights[i] + averaging_weight*weights[i]
                    layer0.set_weights(curr_weights)
        
            for layer in models[0].layers:
                curr_weights = layer.get_weights()
                for i in range(len(curr_weights)):
                    curr_weights[i] = curr_weights[i] / sum_weighted_average
                layer.set_weights(curr_weights)
            print("After")
            for layer in models[0].layers:
                print(layer.get_weights())
                print("\n")
            return models[0]  
    # def save_model(self,model):
    #     import torch
    #     self.model_name = 'model_' + str(self.server_controller.get_version()) + '.pt'
    #     m = torch.jit.script(model)
    #     torch.jit.save(m, 'torch1.pt')
    #     logging.info("Averaged Model has been saved on Server")
    
    def count_average(self):
        try:
            self.barrier.wait()
        except:
            logging.warning('In count_average, barrier broke')
            self.server_controller.version_updating.acquire()
            pass
        averaged_model = self.calculate_average()
        self.server_controller.increase_version()

        whole_path = self.server_model_path + '/' + 'model_' + str(self.server_controller.get_version())
        if self.model_type == "pytorch":
            whole_path += '.pt'
        elif self.model_type == "tensorflow":
            whole_path += '.h5'
        print(whole_path)
        for f in os.listdir(self.server_model_path):
            os.remove(os.path.join(self.server_model_path, f))
        save_model(self.model_type,whole_path,averaged_model)
        # Interrupt server.accept() with fake connection
        fake_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP_address = self.ip
        Port = self.port
        fake_server.connect((IP_address, Port))
        for client_socket in self.received_values:
            client_socket.send(b'calculation completed')
        logging.debug("Poison packet has been sent to the DataChannel server")
        self.server_controller.version_updating.release()

    def check_time(self):
        while True:
            if self.last_time is None:
                continue
            current_time = datetime.datetime.now()
            dif = current_time - self.last_time
            dif = dif.total_seconds()
            if dif > self.gap_time:
                self.barrier.abort()
                logging.debug("Barrier Aborted")
                break

    def client_handler(self, client_socket):
        client_socket.send(b'start')
        client = client_socket.recv(1024)
        client = client.decode('utf-8')
        client_socket.send(b'Id Verified')
        logging.info("ID has been received in datachannel server by {}".format(client_socket.getpeername()))
        if self.barrier.broken:
            client_socket.send(b'I won\'t receive connections anymore!')
            return
        # message = int(client_socket.recv(1024).decode())
        model = receive(client_socket,self.model_type)
        logging.info("Model has been received in datachannel server by {}".format(client_socket.getpeername()))
        if client not in self.clientsDB.get_clients():
            client_socket.send(b'I don\'t know you!')
            print("I don't know you!")
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
