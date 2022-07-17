
import os 
class Validator:
    def __init__(self, yaml_dict):
        self.yaml_dict = yaml_dict
        self.keys = set(['ip', 'datachannel_port', 'ping_port', 'id_path', 'model_type', 'model_path', 'input_path', 'output_path', 'learning_rate', 'client_sleep_time'])
        self.validate()
    
    def validate(self):
        for key in self.keys:
            if key not in self.yaml_dict:
                raise Exception("Key '{}' not found in yaml file".format(key))
        if self.yaml_dict['model_type'] not in ['sklearn', 'tensorflow','pytorch']:
            raise Exception("Model type '{}' not supported".format(self.yaml_dict['model_type']))
        if not os.path.exists(self.yaml_dict['model_path']):
            raise Exception("Model path '{}' not found".format(self.yaml_dict['model_path']))
        if not os.path.exists(self.yaml_dict['input_path']):
            raise Exception("Input path '{}' not found".format(self.yaml_dict['input_path']))
        if not os.path.exists(self.yaml_dict['output_path']):
            raise Exception("Output path '{}' not found".format(self.yaml_dict['output_path']))
        if not os.path.isfile(self.yaml_dict['model_path']):
            raise Exception("Model path '{}' not found".format(self.yaml_dict['model_path']))
        if not os.path.isfile(self.yaml_dict['input_path']):
            raise Exception("Input path '{}' not found".format(self.yaml_dict['input_path']))
        if not os.path.isfile(self.yaml_dict['output_path']):
            raise Exception("Output path '{}' not found".format(self.yaml_dict['output_path']))

        
        
