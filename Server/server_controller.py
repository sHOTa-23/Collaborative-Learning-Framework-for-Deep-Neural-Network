import threading

class ServerController:
    def __init__(self,datachanel_server,ping_server,version=0):
        self.datachanel_server = datachanel_server
        self.ping_server = ping_server
        self.version = version
        self.version_updating = threading.Lock()
        self.version_lock = threading.Lock()
    
    def start(self):
        self.ping_server.start(self)

    def fire(self):
        self.datachanel_server.start(self)

    def get_version(self):
        self.version_lock.acquire()
        cur_version = self.version
        self.version_lock.release()
        return cur_version

    def increase_version(self):
        self.version_lock.acquire()
        self.version = self.version + 1
        self.version_lock.release()
   