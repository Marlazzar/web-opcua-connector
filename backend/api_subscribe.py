# methods for managing node subscriptions
import backend.globals as gl
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from asyncua import ua
from backend.utils import dict_keys_list


bp = Blueprint('subs', __name__, url_prefix='/subs')


@bp.route('/subscribe')
def subscribe():
    # datachange subscription
    if not gl.uaclient._connected:
        return jsonify("client not connected")
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        node = gl.uaclient.get_node(f"ns={ns};i={id}")
        gl.uaclient.subscribe_datachange(node, gl.handler)
        #sub = uaclient.client.create_subscription(100, handler)
        #handle = sub.subscribe_data_change(node)
        return jsonify("subscribed")
    else:
        return jsonify("specify id and ns")


@bp.route('/unsubscribe')
def unsubscribe():
    if not gl.uaclient._connected:
        return jsonify("client not connected")
    if 'id' in request.args and 'ns' in request.args:
        id = int(request.args['id'])
        ns = int(request.args['ns'])
        if (id, ns) in gl.subscribed_nodes:
            node = gl.uaclient.get_node(f"ns={ns};i={id}")
            gl.uaclient.unsubscribe_datachange(node)
            gl.subscribed_nodes.pop((id, ns))
            return jsonify("unsubscribed")
        else:
            return jsonify("node wasn't found in subscriptions"), 500
    else:
        return jsonify("specify id and ns"), 501


@bp.route('/get_sub')
def get_sub():
    if not gl.uaclient._connected:
        return jsonify("client not connected")
    if 'id' in request.args and 'ns' in request.args:
        id = int(request.args['id'])
        ns = int(request.args['ns'])
        if (id, ns) not in gl.subscribed_nodes:
            return jsonify("no subscription found")
        # this should return the value by the last event...
        # but if i do it like that, frontend would have to poll this all the time.
        return jsonify(gl.subscribed_nodes[(id, ns)])
    else:
        return jsonify("specify id and ns")


@bp.route('/subscribed_nodes')
def subscripted_nodes():
    return jsonify(dict_keys_list(gl.subscribed_nodes))

