# from torch import nn
# import torch
# seq_size = 3
# input_size = 500

# model = nn.Sequential(nn.Linear(1500,750),
#                       nn.ReLU(),
#                       nn.Linear(750, 500),
#                       nn.Softmax())
# m = torch.jit.script(model)
# torch.jit.save(m, 'bla.pt')
# print(model)
# input = torch.randn(3000)
import torch
from dataset import Dataset
class Model:
    def __init__(self,model_path,dataset):
        self.model_path =model_path
        self.model = torch.jit.load(self.model_path)
        self.dataset = dataset
    def predict(self,words,num_words):
        vector = self.dataset.prepare_words(words)
        return self.dataset.get_words_from_prediction(self.model(vector).detach().numpy(),num_words)


# model = torch.jit.load('bla.pt')
# input = torch.randn((2,1500))
# input1 = torch.randn(1500)
# inputt2 = torch.randn(1500)
# input = torch.cat((input1,inputt2)).reshape(2,1500)
# print(model(input).shape)


# model = Model('bla.pt','a.txt')
# print(model.predict("მე და შენ".split(" "),3))







