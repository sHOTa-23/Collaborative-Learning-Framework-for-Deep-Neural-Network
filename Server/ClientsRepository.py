from pymongo import MongoClient

class ClientsRepository:
    def __init__(self,mongodb_host):
        self.con = MongoClient(mongodb_host)
        self.db = self.con.clientsDB
        self.clients = self.db.ids
        # self.clients = []

    def add_client(self, id):
        self.clients.insert_one({'id': id})
        # self.clients.append(id)

    def get_clients(self):
        cur_clients = [client['id'] for client in self.clients.find()]
        return cur_clients
        # return self.clients