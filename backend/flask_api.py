import flask
from flask import request, jsonify
import sys
sys.path.insert(0,'..')
from opcua.opcua_client import UaClient
from methods import generate_tree, create_desc_dict

app = flask.Flask(__name__)
app.config["DEBUG"] = True

uaclient = UaClient()
#url = "opc.tcp://localhost:4840/freeopcua/server/"


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
            return str(e)
    if uaclient._connected:
        return jsonify("connected")
    else:
        return jsonify("not connected")

@app.route("/post_connect")
def post_connect():
    return """
        <html>
            <body>
                <form action = "http://localhost:5000/connect" method = "post">
                    <p>OPCUA Server:</p>
                    <p><input type = "text" name = "url" /></p>
                    <p><input type = "submit" value = "submit" /></p>
                </form>
            </body>
        </html>
    """
    
@app.route('/disconnect', methods=['GET'])
def disconnect():
    uaclient.disconnect()
    return jsonify("disconnected")


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
        return children
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
def get_node_desc():
    if 'id' in request.args and 'ns' in request.args:
        id = request.args['id']
        ns = request.args['ns']
        if uaclient._connected:
            node = uaclient.get_node(f"ns={ns};i={id}")
            desc = UaClient.get_node_desc(node)
            desc = create_desc_dict(desc)
            return jsonify(desc)
        return "client not connected"
    else:
        return "specify id and ns (namespace)"


if __name__ == '__main__':
    app.run(debug=True)
