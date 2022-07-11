import torch
import torch.nn as nn
import torch.nn.functional as F
from t1 import Net
lr = 1.5
MSE_loss_fn = nn.MSELoss()
model = torch.jit.load('model_scripted.pt')
model.eval()
input = torch.randn(1, 1, 32, 32)
out = model(input)
out.requires_grad
c = torch.Tensor([[ 0.0656, -0.0524, -0.0208, -0.0310, -0.0672, -0.0786, -0.0219, -0.1383,
         -0.0584, -0.1289]])
loss = MSE_loss_fn(out, c)
loss.backward()
a = model.conv1.weight.grad
print(model.conv1.weight[0, 0])
with torch.no_grad():
    for param in model.parameters():
        param -= param.grad * lr
print(model.conv1.weight[0, 0])
model_scripted = torch.jit.script(model) # Export to TorchScript
model_scripted.save('model_scripted.pt')
# print(model.conv1.weight==a)