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
    def __init__(self,model_path,text_path):
        self.model_path =model_path
        self.model = torch.jit.load(self.model_path)
        self.dataset = Dataset(text_path)
    def predict(self,words,num_words):
        words = [self.dataset.remove_punct(word) for word in words]
        tokens = [self.dataset.get_one_hot_vector(token) for token in words]
        vector = []
        for token in tokens:
            vector.extend(token)
        vector = torch.tensor(vector, dtype=torch.float32)
        return self.dataset.get_words_from_prediction(self.model(vector).detach().numpy(),num_words)

# model = Model('bla.pt','a.txt')
# print(model.predict("მე და შენ".split(" "),3))







