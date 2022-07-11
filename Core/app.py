import yaml
from Core.client import Client
from Server.server import Server

#178.62.92.57
class App:
    def __init__(self,configuration_path) -> None:
        self.configuration_path = configuration_path
        self.configuration = self.load_configuration()
    
    def load_configuration(self) -> dict:
        with open(self.configuration_path) as f:
            return yaml.safe_load(f)
    def run(self):
        server = Server(self.configuration['ip'],self.configuration['port'])
        client = Client(self.configuration['ip'],self.configuration['port'])

        
        
    
    
        