from pymongo import MongoClient

class ModelAccuraciesRepository:
    def __init__(self,mongodb_host):
        self.con = MongoClient(mongodb_host)
        self.db = self.con.clientsDB
        self.models = self.db.models

    def add_model_accuracy(self, accuracy, time, clients):
        self.models.insert_one({'accuracy': accuracy, 'time': time, 'clients': clients})

    def get_clients_accuracies(self):
        accuracies = [(model['time'], model['clients'], model['accuracy']) for model in self.models.find()]
        return accuracies
