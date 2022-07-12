class Controller:
    def __init__(self,datachanel_client,ping_client):
        self.datachanel_client = datachanel_client
        self.ping_client = ping_client
    
    def start(self):
        self.ping_client.start(self)

    def fire(self):
        self.datachanel_client.start()