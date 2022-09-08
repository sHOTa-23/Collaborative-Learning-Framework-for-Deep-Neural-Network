# Collaborative Learning Framework For Deep Neural Network
This repository is our implementation of Google's [Federated Learning Paper. ](https://arxiv.org/pdf/1812.02903.pdf) 

We help developers retrain their neural networks on the devices of their clients without transferring any of the clients' data.



## Setting up the environment
In order to use everything in this repository, you need to install the following dependencies:
```bash
pymongo==4.2.0 - #for server side
PyYAML==5.3.1
torch==1.12.0 #- if you have pytorch model
tensorflow==2.3.0 #-if you have tensorflow model
Flask==2.2.2 #for server side
```
For installing that dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```
## Abstract
The project is divided into two sections: one for the server side and one for the client side. You must fill out a YAML configuration file and then specify the path to it in the integration part in order to set up a server.

Server configuration file looks like this:
```yml
ip : 127.0.0.1 #ip address of the server.
datachannel_port : 9920 #port for the training part of the server.
ping_port : 9921 #port for the pinging and navigating clients.
chart_port: 8080 #port for online board, where to check activities of the users and metric changes toward iterations.
mongodb_host : mongodb+srv://doadmin:g12k79jU8L3y0u5t@db-mongodb-nyc3-12601-daeda50b.mongo.ondigitalocean.com/admin?authSource=admin&replicaSet=db-mongodb-nyc3-12601&tls=true #mongodb host
model_type : pytorch #framework of the model currently we support pytorch and tensorflow
server_model_path: models/server/ #path to a starting model which is uploaded to the server. 
datachannel_time_interval: 60 # retraining time interval(seconds)
datachannel_gap_time: 20 #time interval (seconds) to wait for new clients before calculating the average of the model.
golden_data_input_path: goldeninp.pkl  #golden input data path. Must be in pickle format
golden_data_output_path: goldenout.pkl #golden output data path. Must be in pickle format
```
Client side configuration file looks like this:
```yaml
ip : 159.223.129.45 #ip address of the server.
datachannel_port : 9920 #port for the training part of the server.
ping_port : 9921 #port for the pinging and navigating to server.
id_path : id.txt #path where the id will be stored 
client_sleep_time : 1 #Time interval(seconds) of pinging the server.
model_path : bla.pt #path to the model on the device
model_type : pytorch  #framework of the model currently we support pytorch and tensorflow
input_path: inp.pkl #directory where the input will be saved by the developer's application
output_path: out.pkl #directory where the output will be saved by the developer's application
learning_rate : 1.7 #learning rate for the iteration (optional)
```

## Installation
In order to install server side, run:
```bash
pip install Federated-Learning-Server
```
For client side, run:
```bash
pip install Federated-Learning-Client
```

## Usage

In order to use our framework first you need to start the server. For that you need to integrate these lines into your code:
```python
from Server.app_servers import AppServer

# score function to calculate your chosen metric
def score_fn(pred,golden):
    ans_index = golden.argmax(dim=1)
    score = (pred.argmax(dim=1) == ans_index).sum().item()/ans_index.shape[0]
    return score

app = AppServer('path_to_server_configuration_file',score_fn)
app.run()
```
For client integration you need to put these lines into your code:
```python
from Client.app_clients import AppClient
loss = nn.MSELoss() # loss function of your choice
app = AppClient('conf.yml',loss)
app.run()
```
Integrating our framework in your system is easy, it just takes few lines of code for both client and server sides.

## Testing
For testing you can use the following command:
```bash
./test.bat # for windows
./test.sh # for ubuntu
```
