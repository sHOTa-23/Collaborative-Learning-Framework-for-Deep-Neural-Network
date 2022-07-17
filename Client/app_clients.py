import yaml
from Client.datachannel_client import DatachannelClient
from Client.ping_client import PingClient
from Client.yaml_validator import Validator
from Client.client_controller import ClientController
import logging
logging.basicConfig(level=logging.NOTSET)

#178.62.92.57
class AppClient:
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
        ping_client = PingClient(self.configuration['ip'],self.configuration['ping_port'],self.configuration['id_path'],self.configuration['model_path'],self.configuration['model_type'],self.configuration['client_sleep_time'])        
        datachannel_client = DatachannelClient(self.configuration['ip'],self.configuration['datachannel_port'],self.configuration['model_type'],self.configuration['model_path'],self.configuration['input_path'],self.configuration['output_path'],self.configuration['id_path'],self.configuration['learning_rate'],self.loss_function,self.optimizer)

        client_controller = ClientController(datachannel_client,ping_client)
        client_controller.start()

        logging.debug("Client Controller started")