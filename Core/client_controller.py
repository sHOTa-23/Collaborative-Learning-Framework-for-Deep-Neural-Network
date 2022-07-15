import threading

class ClientController:
    def __init__(self,datachanel_client,ping_client):
        self.datachanel_client = datachanel_client
        self.ping_client = ping_client
        self.version_lock = threading.Lock()
        self.version = 0
        self.updating_lock = threading.Lock()
    
    def start(self):
        self.ping_client.start(self)
        self.datachanel_client.set_controller(self)

    def fire(self):
        import datetime
        import logging
        logging.info("Fire happened in controller" + str(datetime.datetime.now().strftime("%H:%M:%S")))
        self.datachanel_client.start(self)
    
    def fire_ping(self):
        self.ping_client.change_status()

    def get_version(self):
        self.version_lock.acquire()
        cur_version = self.version
        self.version_lock.release()
        return cur_version

    def set_version(self, new_version):
        self.version_lock.acquire()
        self.version = new_version
        self.version_lock.release()