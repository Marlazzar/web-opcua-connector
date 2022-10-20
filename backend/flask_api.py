import flask
from flask import request, jsonify
import sys
from asyncua import ua
from opcua_client import UaClient
from methods import create_desc_dict, dict_keys_list
import logging
from DatachangeHandler import DatachangeHandler
import os

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

uaclient = UaClient()
# problem: this ip will probably change. don't know where exampleserver will run...
default_url = "opc.tcp://localhost:4840/freeopcua/server/"

# subscribednodes will have the following form:
# dictionary key: (id, ns) value: dict(nodeid, namespace, value, timestamp)
subscribed_nodes = {}
# update_datachage method should receive dict(nodeid, namespace, value, timestamp) as parameter and edit
# this list
def update_datachange(nodedict):
    # called once even for const
    id = nodedict["NodeId"]
    ns = nodedict["Namespace"]
    subscribed_nodes[(id,ns)] = nodedict

handler = DatachangeHandler(update_datachange)



@app.route('/', methods=['GET'])
def default():
    return jsonify("this is my flask backend")


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    subscribed_nodes.clear()
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

# only for debugging backend without frontend
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
    # returns description of all the children of specified node. gives the following child-attributes:
    # nodeid, namespace, displayname, nodeclass
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


@app.route('/subscribe')
def subscribe():
    # datachange subscription
    if not uaclient._connected:
        return jsonify("client not connected")
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        node = uaclient.get_node(f"ns={ns};i={id}")
        sub = uaclient.client.create_subscription(100, handler)
        handle = sub.subscribe_data_change(node)
        return jsonify("subscribed")
    else:
        return jsonify("specify id and ns")


# TODO: unsubscribe method

@app.route('/get_sub')
def get_sub():
    if not uaclient._connected:
        return jsonify("client not connected")
    if 'id' in request.args and 'ns' in request.args:
        id = int(request.args['id'])
        ns = int(request.args['ns'])
        if (id, ns) not in subscribed_nodes:
            return jsonify("no subscription found")
        # this should return the value by the last event...
        # but if i do it like that, frontend would have to poll this all the time.
        return jsonify(subscribed_nodes[(id, ns)])
    else:
        return jsonify("specify id and ns")


@app.route('/subscripted_nodes')
def subscripted_nodes():
    return jsonify(dict_keys_list(subscribed_nodes))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
