class ClientController:
    def __init__(self,datachanel_client,ping_client):
        self.datachanel_client = datachanel_client
        self.ping_client = ping_client
    
    def start(self):
        self.ping_client.start(self)
        self.datachanel_client.set_controller(self)

    def fire(self):
        import datetime
        import logging
        logging.info("Fire happened in controller" + str(datetime.datetime.now().strftime("%H:%M:%S")))
        self.datachanel_client.start()
    
    def fire_ping(self):
        self.ping_client.change_status()