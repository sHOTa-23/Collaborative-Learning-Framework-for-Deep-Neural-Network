
import os 
class Validator:
    def __init__(self, yaml_dict):
        self.yaml_dict = yaml_dict
        self.keys = set(['ip', 'datachannel_port', 'ping_port','mongodb_host', 'model_type', 'server_model_path', 'datachannel_time_interval', 'datachannel_gap_time'])
        self.validate()
    
    def validate(self):
        for key in self.keys:
            if key not in self.yaml_dict:
                raise Exception("Key '{}' not found in yaml file".format(key))
        if self.yaml_dict['model_type'] not in ['sklearn', 'tensorflow','pytorch']:
            raise Exception("Model type '{}' not supported".format(self.yaml_dict['model_type']))
        if not os.path.exists(self.yaml_dict['server_model_path']):
            raise Exception("Model path '{}' not found".format(self.yaml_dict['server_model_path']))

        
        
