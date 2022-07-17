from Server.app_servers import AppServer
import torch.nn as nn

app = AppServer('Server/conf.yml')
app.run()
