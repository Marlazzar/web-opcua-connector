import flask
from flask import request, jsonify
from opcua.opcua_client import UaClient
import json
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
    uaclient.disconnect()
    return 'disconnected'


@app.route('/children')
def get_children():
    if not uaclient._connected:
        return 'not connected'

    if 'id' in request.args:
        id = int(request.args['id'])
        node = uaclient.get_node(id)
        children = uaclient.get_children(node)
        return children
    else:
        node = uaclient.client.nodes.root
        children = uaclient.get_children(node)
        return children


@app.route('/nodes')
def get_node_desc():
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        if uaclient._connected:
            node = uaclient.get_node(f"ns={ns};i={id}")
            desc = UaClient.get_node_desc(node)
            return jsonify(desc)
        return "client not connected"
    else:
        return "Error: No id and/or no ns (namespace) field provided. Please specify id and ns."


if __name__ == '__main__':
    app.run(debug=True)
