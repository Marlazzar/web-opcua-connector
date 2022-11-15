# api methods for navigating/browsing opcua server nodes
import backend.globals as gl
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from backend.utils import create_desc_dict
from asyncua import ua


bp = Blueprint('browse', __name__, url_prefix='/browse')


@bp.route("/", methods=["GET"])
def browse():
    return "browse"


# only for debugging backend without frontend
# doesn't work if you run this in a docker container,
# cause default url references localhost.
@bp.route("/temporary_connect", methods=['GET'])
def temporary_connect():
    default_url = "opc.tcp://localhost:4840/"
    gl.uaclient.connect(default_url)
    return jsonify(gl.uaclient._connected)


@bp.route('/root', methods=['GET'])
def root():
    root = gl.uaclient.client.nodes.root
    description = gl.uaclient.get_node_desc(root)
    description = create_desc_dict(description)
    return jsonify(description)


@bp.route('/children')
def get_children():
    # returns description of all the children of specified node. gives the following child-attributes:
    # nodeid, namespace, displayname, nodeclass
    if not gl.uaclient._connected:
        return 'not connected'
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        node = gl.uaclient.get_node(f"ns={ns};i={id}")
        children = gl.uaclient.get_children(node)
        children = [create_desc_dict(ch) for ch in children]
        return jsonify(children)
    else:
        return "specify id and ns (namespace)"


@bp.route('/nodes')
def get_node_attributes():
    # this method returns specified attributes of the node
    # what attributes do we want? 
    attrs = [ua.AttributeIds.BrowseName, ua.AttributeIds.DisplayName, ua.AttributeIds.DataType, ua.AttributeIds.MinimumSamplingInterval, ua.AttributeIds.NodeId, ua.AttributeIds.Value, ua.AttributeIds.NodeClass]
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        if gl.uaclient._connected:
            node = gl.uaclient.get_node(f"ns={ns};i={id}")
            attributes = gl.uaclient.get_all_attributes(node, all=False, attributes=attrs)
            return jsonify(attributes)
        return jsonify("client not connected")
    else:
        return jsonify("specify id and ns (namespace)")
