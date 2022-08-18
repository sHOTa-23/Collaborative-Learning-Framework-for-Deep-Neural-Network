import sys
sys.path.insert(0,"..")

from Server.app_servers import AppServer
import torch.nn as nn
import torch
def score_fn(pred,golden):
    ans_index = golden.argmax(dim=1)
    return (pred.argmax(dim=1) == ans_index).sum().item()/ans_index.shape[0]

# app = AppServer('../Server/conf.yml')
# app.run()

print(score_fn(torch.tensor([[0.3,0.45,0.25],[0.1,0.8,0.1],[0.98,0.01,0.01]]),torch.tensor([[1,0,0],[0,1,0],[1,0,0]])))
