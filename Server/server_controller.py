class ServerController:
    def __init__(self,datachanel_server,ping_server):
        self.datachanel_server = datachanel_server
        self.ping_server = ping_server
    
    def start(self):
        self.ping_server.start(self)

    def fire(self):
        self.datachanel_server.start()