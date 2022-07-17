import yaml
from Server.datachannel_server import DatachannelServer
from Server.ping_server import PingServer
from Server.yaml_validator import Validator
from Server.server_controller import ServerController
from Client.ClientsRepository import ClientsRepository
import logging
logging.basicConfig(level=logging.NOTSET)

#178.62.92.57
class AppServer:
    def __init__(self,configuration_path) -> None:
        self.configuration_path = configuration_path
        self.configuration = self.load_configuration()
    
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
        ping_server = PingServer(self.configuration['ip'],self.configuration['ping_port'],clientDB,self.configuration['server_model_path'],self.configuration['model_type'])
        datachannel_server = DatachannelServer(self.configuration['ip'],self.configuration['datachannel_port'],clientDB,self.configuration['server_model_path'],self.configuration['model_type'])
        
        server_controller = ServerController(datachannel_server,ping_server)
        server_controller.start()

        logging.debug("Server Controller started")