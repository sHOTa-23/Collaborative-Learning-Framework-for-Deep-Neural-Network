from pymongo import MongoClient

class PingClientsRepository:
    def __init__(self,mongodb_host):
        self.con = MongoClient(mongodb_host)
        self.db = self.con.clientsDB
        self.clientsPings = self.db.clientsPings

    def add_client_ping(self, id, time):
        self.clientsPings.insert_one({'id': id, 'time': time})

    def get_clients_pings(self):
        pings = [(client['id'], client['time']) for client in self.clientsPings.find()]
        return pings
