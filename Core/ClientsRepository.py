from pymongo import MongoClient

class ClientsRepository:
    def __init__(self):
        self.con = MongoClient('mongodb://localhost:27017/')
        self.db = self.con.clientsDB
        self.clients = self.db.ids

    def add_client(self, id):
        self.clients.insert_one({'id': id})

    def get_clients(self):
        cur_clients = [client['id'] for client in self.clients.find()]
        return cur_clients
