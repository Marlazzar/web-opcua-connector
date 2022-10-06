import flask
from flask import request, jsonify
import sys
from asyncua import ua
sys.path.insert(0,'..')
from opcua.opcua_client import UaClient
from methods import generate_tree, create_desc_dict
import logging

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

uaclient = UaClient()
default_url = "opc.tcp://localhost:4840/freeopcua/server/"


@app.route('/', methods=['GET'])
def default():
    return 'home'

@app.route('/home', methods=['GET'])
def home():
    return jsonify("home")

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    url = request.json['url']
    print(url)
    if request.method == 'POST':
        try:
            uaclient.connect(url)
        except Exception as e:
            return "failed to connect to opcua server", 404
    if uaclient._connected:
        return jsonify("connected")
    else:
        return jsonify("not connected")

@app.route("/temporary_connect", methods=['GET'])
def temporary_connect():
    uaclient.connect(default_url)
    return jsonify(uaclient._connected)

@app.route('/disconnect', methods=['GET'])
def disconnect():
    uaclient.disconnect()
    return jsonify("disconnected")

@app.route('/root', methods=['GET'])
def root():
    root = uaclient.client.nodes.root
    description = uaclient.get_node_desc(root)
    description = create_desc_dict(description)
    return jsonify(description)

@app.route('/children')
def get_children():
    if not uaclient._connected:
        return 'not connected'
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        node = uaclient.get_node(f"ns={ns};i={id}")
        children = uaclient.get_children(node)
        children = [create_desc_dict(ch) for ch in children]
        return jsonify(children)
    else:
        return "specify id and ns (namespace)"


@app.route('/tree')
def tree():
    if not uaclient._connected:
        return 'not connected'
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        node = uaclient.get_node(f"ns={ns};i={id}")
        tree = generate_tree(node, uaclient)
        return jsonify(tree)
    else:
        return "specify id and ns (namespace)"

@app.route('/nodes')
def get_node_attributes():
    # this method returns specified attributes of the node
    # what attributes do we want? 
    attrs = [ua.AttributeIds.BrowseName, ua.AttributeIds.DisplayName, ua.AttributeIds.DataType, ua.AttributeIds.MinimumSamplingInterval, ua.AttributeIds.NodeId, ua.AttributeIds.Value, ua.AttributeIds.NodeClass]
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        if uaclient._connected:
            node = uaclient.get_node(f"ns={ns};i={id}")
            attributes = uaclient.get_all_attributes(node, all=False, attributes=attrs)
            return jsonify(attributes)
        return jsonify("client not connected")
    else:
        return jsonify("specify id and ns (namespace)")


if __name__ == '__main__':
    app.run(debug=True)
