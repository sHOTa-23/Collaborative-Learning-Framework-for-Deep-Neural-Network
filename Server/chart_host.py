from flask import Flask, send_from_directory
import yaml

conf = None
with open('conf.yml') as f:
    conf = yaml.safe_load(f)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def static_dir():
    return send_from_directory("", conf['chart_path'])

if __name__ == '__main__':
    app.run(host=conf['ip'], port='8080')
