import yaml
from Core.datachannel_client import DatachannelClient
from Server.datachannel_server import DatachannelServer
from Core.ping_client import PingClient
from Server.ping_server import PingServer

#178.62.92.57
class App:
    def __init__(self,configuration_path) -> None:
        self.configuration_path = configuration_path
        self.configuration = self.load_configuration()
    
    def load_configuration(self) -> dict:
        with open(self.configuration_path) as f:
            return yaml.safe_load(f)

    def run(self):
        datachannelServer = DatachannelServer(self.configuration['ip'],self.configuration['datachannel_port'])
        datachannelClient = DatachannelClient(self.configuration['ip'],self.configuration['datachannel_port'],self.configuration['model_type'],self.configuration['model_path'],self.configuration['input_path'],self.configuration['output_path'],self.configuration['learning_rate'])
      #  pingServer = PingServer(self.configuration['ip'],self.configuration['ping_port'])
       # pingClient = PingClient(self.configuration['ip'],self.configuration['ping_port'],self.configuration['id_path'],self.configuration['client_sleep_time'])
