import flask
from flask import request, jsonify
from opcua.opcua_client import UaClient
import asyncio

app = flask.Flask(__name__)
app.config["DEBUG"] = True

uaclient = UaClient()
url = "opc.tcp://localhost:4840/freeopcua/server/"


@app.route('/', methods=['GET'])
def home():
    return 'home'


@app.route('/connect', methods=['GET'])
def connect():
    uaclient.connect(url)
    if uaclient._connected:
        return 'connection success'
    else:
        return 'connection failed'


@app.route('/disconnect', methods=['GET'])
def disconnect():
    print("disconnect")
    uaclient.disconnect()
    return 'disconnected'

app.run(debug=True)
