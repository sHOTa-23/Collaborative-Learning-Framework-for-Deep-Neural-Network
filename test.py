from Core.app import App
import torch.nn as nn
app = App('Core/conf.yml',nn.L1Loss())
app.run()
