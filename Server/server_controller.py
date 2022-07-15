import threading

class ServerController:
    def __init__(self,datachanel_server,ping_server):
        self.datachanel_server = datachanel_server
        self.ping_server = ping_server
        self.version = 0
        self.version_updating = threading.Lock()
    
    def start(self):
        self.ping_server.start(self)

    def fire(self):
        self.datachanel_server.start(self)

    def get_version(self):
        return self.version

    def increase_version(self):
        self.version = self.version + 1
   