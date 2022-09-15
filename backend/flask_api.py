import flask
from flask import request, jsonify
from opcua.opcua_client import UaClient
import json
import asyncio

app = flask.Flask(__name__)
app.config["DEBUG"] = True

uaclient = UaClient()
url = "opc.tcp://localhost:4840/freeopcua/server/"


def node_repr(node):
    return node.nodeid


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
def get_node():
    if 'id' in request.args:
        id = int(request.args['id'])
        if uaclient._connected:
            node = uaclient.get_node(nodeid=id)
            return jsonify(node_repr(node))
        return 'client not connected'
    else:
        return "Error: No id field provided. Please specify an id."

uaclient.connect(url)
root = uaclient.client.nodes.root
children = uaclient.get_children(root)
print(type(root))
print(node_repr(root))
app.run(debug=True)
