import yaml
from Server.datachannel_server import DatachannelServer
from Server.ping_server import PingServer
from Core.yaml_validator import Validator
from Server.server_controller import ServerController
from Core.ClientsRepository import ClientsRepository
import logging
logging.basicConfig(level=logging.NOTSET)

#178.62.92.57
class AppServer:
    def __init__(self,configuration_path,loss_function,optimizer = None) -> None:
        self.configuration_path = configuration_path
        self.configuration = self.load_configuration()
        self.loss_function = loss_function
        self.optimizer = optimizer
    
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
        ping_server = PingServer(self.configuration['ip'],self.configuration['ping_port'],clientDB)
        datachannel_server = DatachannelServer(self.configuration['ip'],self.configuration['datachannel_port'],clientDB)
        
        server_controller = ServerController(datachannel_server,ping_server)
        server_controller.start()

        logging.debug("Server Controller started")