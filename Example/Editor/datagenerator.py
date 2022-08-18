# import sys
# sys.path.insert(0,"../../")
# from dataset import Dataset
# import torch.nn as nn
# dataset = Dataset('a.txt',3)
# sent1 = "საქართველოს დედაქალაქი არის თბილისი და მე ვარ მისი მოქალაქე და ვლაპარაკობ ქართულად".split()
# dataset.save_words_in_pickle(sent1,'goldeninp.pkl','goldenout.pkl')

from torch import nn
import torch
import pickle
seq_size = 3
input_size = 500

model = nn.Sequential(nn.Linear(3,3))

model1 = nn.Sequential(nn.Linear(3,3))
# with torch.no_grad():
#     for i in model.parameters():
#         print(i)
# print("++++++++++")
# with torch.no_grad():
#     for i in model.parameters():
#         print(i)
with torch.no_grad():
    for (i,j) in zip(model.parameters(),model1.parameters()):
        print(i)
        print("+++++")
        print(j)
        print("________")
        i+=(15*j) 
        print(i)
        print("========")
print("_______________________________________________________")
# with torch.no_grad():
#     for i in model.parameters():
#         print(i)
# accuracy = (pred == out).sum().item()/out.shape[0]