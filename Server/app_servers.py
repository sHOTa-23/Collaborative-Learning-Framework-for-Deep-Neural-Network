import yaml
import os
from Server.datachannel_server import DatachannelServer
from Server.ping_server import PingServer
from Server.yaml_validator import Validator
from Server.server_controller import ServerController
from Server.ClientsRepository import ClientsRepository
import logging
logging.basicConfig(level=logging.NOTSET)

#178.62.92.57
class AppServer:
    def __init__(self,configuration_path,score_fn) -> None:
        print(configuration_path)
        self.configuration_path = configuration_path
        self.configuration = self.load_configuration()
        self.score_fn = score_fn
        with open("droebit.txt", "w+") as f:
            f.write(str(self.configuration['datachannel_time_interval']))
        print(self.configuration)
    
    def load_configuration(self) -> dict:
        with open(self.configuration_path) as f:
            return yaml.safe_load(f)

    def run(self):
        validator = Validator(self.configuration)
        try:
            validator.validate()
        except Exception as e:
            logging.error(e)
            return
        logging.debug("Configuration is valid")
        clientDB = ClientsRepository(self.configuration['mongodb_host'])
        ping_server = PingServer(self.configuration['ip'],self.configuration['ping_port'],clientDB,self.configuration['server_model_path'],self.configuration['model_type'], self.configuration['datachannel_time_interval'])
        datachannel_server = DatachannelServer(self.configuration['ip'],self.configuration['datachannel_port'],clientDB,self.configuration['server_model_path'],self.configuration['model_type'],self.configuration['golden_data_input_path'],self.configuration['golden_data_output_path'],self.score_fn, self.configuration['datachannel_gap_time'])
        
        path = self.configuration['server_model_path']
        highest_version = 0
        for f in os.listdir(path):
            cur_version = int(f[f.find('_')+1:f.find('.')])
            highest_version = max(highest_version, cur_version)

        server_controller = ServerController(datachannel_server,ping_server,highest_version)
        server_controller.start()

        logging.debug("Server Controller started")