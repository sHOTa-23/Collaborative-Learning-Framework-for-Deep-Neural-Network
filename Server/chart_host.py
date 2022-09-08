from flask import Flask, send_from_directory
import yaml
from Server.generate_chart import generate_chart
app = Flask(__name__)
print("app runned")
mongodb_host = None
def run_chart_server(ip,port,mongodb_host_):
    global mongodb_host
    mongodb_host = mongodb_host_
    conf = None
    print("N_____________________")
    app.run(host=ip, port=port)
    
@app.route('/', methods=['GET'])
def static_dir():
    html = generate_chart(mongodb_host)
    return html

    
