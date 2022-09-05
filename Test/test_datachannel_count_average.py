import sys
sys.path.insert(0,"../")
from Server.datachannel_server import DatachannelServer
from Server.ClientsRepository import ClientsRepository
from Client.utils import load_model
import torch
import yaml
from test_utils import *

conf = None
with open('server_conf.yml') as f:
    conf = yaml.safe_load(f)

def score_fn(pred,golden):
    ans_index = golden.argmax(dim=1)
    score = (pred.argmax(dim=1) == ans_index).sum().item()/ans_index.shape[0]
    if score == 0:
        return 0.5
    return score

def test_count_average_pytorch():
    res = True
    datachannel_server = DatachannelServer('127.0.0.1', 9961, ClientsRepository(conf["mongodb_host"]), "", "pytorch", "goldeninp.pkl", "goldenout.pkl", score_fn)
    model1 = load_model("pytorch", "pytorch_models_for_average/model1.pt")
    model2 = load_model("pytorch", "pytorch_models_for_average/model1.pt")
    with torch.no_grad():
        for i in model1.parameters():
            i*=0.3
    model3 = model1
    with torch.no_grad():
        for i in model3.parameters():
            i*=0.5
        for (i,j) in zip(model3.parameters(),model2.parameters()):
            i+=0.5*j
    datachannel_server.received_values[1] = model1
    datachannel_server.received_values[2] = model2
    averaged_model = datachannel_server.calculate_average()
    res = res and assert_equals(model3, averaged_model, "Model averaged incorrectly!!")
    return res

def test_count_average_tensorflow():
    res = True
    datachannel_server = DatachannelServer('127.0.0.1', 9961, ClientsRepository(conf["mongodb_host"]), "", "tensorflow", "goldeninp.pkl", "goldenout.pkl", score_fn)
    model1 = load_model("tensorflow", "pytorch_models_for_average/tf.h5")
    model2 = load_model("tensorflow", "pytorch_models_for_average/tf.h5")
    for layer in model1.layers:
        curr_weights = layer.get_weights()
        for i in range(len(curr_weights)):
            curr_weights[i] = curr_weights[i] * 0.3
        layer.set_weights(curr_weights)
    model3 = model1
    for layer in model3.layers:
        curr_weights = layer.get_weights()
        for i in range(len(curr_weights)):
            curr_weights[i] = curr_weights[i] * 0.5
        layer.set_weights(curr_weights)
    for (layer0,layer1) in zip(model3.layers,model2.layers):
        curr_weights = layer0.get_weights()
        weights = layer1.get_weights()
        for i in range(len(curr_weights)):
            curr_weights[i] = curr_weights[i] + weights[i]*0.5
        layer0.set_weights(curr_weights)
    datachannel_server.received_values[1] = model1
    datachannel_server.received_values[2] = model2
    averaged_model = datachannel_server.calculate_average()
    res = res and assert_equals(model3, averaged_model, "Model averaged incorrectly!!")
    return res

# final_score(test_count_average_pytorch)
final_score(test_count_average_tensorflow)
