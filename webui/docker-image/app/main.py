from flask import Flask
import logging

# the all-important app variable:
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to PEON. The game server manager."

if __name__ == "__main__":
    logging.basicConfig(filename='/var/log/peon/webui.log', filemode='a', format='%(asctime)s %(thread)d [%(levelname)s] - %(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0', debug=True, port=80)