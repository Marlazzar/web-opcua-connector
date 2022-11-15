
from flask import Flask
import backend.api_browse as api_browse
import backend.api_subscribe as api_subscribe
import backend.globals as gl
from flask import jsonify, request

def register_base_urls(flaskapp):
    # a simple page that says hello
    @flaskapp.route('/')
    def hello():
        return "This is my flask backend" 

    # catch all undefined paths
    @flaskapp.route('/', defaults={'path': ''})
    @flaskapp.route('/<path:path>')
    def catch_all(path):
        return jsonify("Backend says there is nada here!"), 500


    @flaskapp.route('/connect', methods=['GET', 'POST'])
    def connect():
        gl.subscribed_nodes.clear()
        url = request.json['url']
        if request.method == 'POST':
            try:
                gl.uaclient.connect(url)
            except Exception as e:
                return jsonify("failed to connect to opcua server"), 500
        if gl.uaclient._connected:
            return jsonify("connected")
        else:
            return jsonify("not connected")

    @flaskapp.route('/disconnect', methods=['GET'])
    def disconnect():
        gl.uaclient.disconnect()
        return jsonify("disconnected")




def create_app(test_config=None):
    gl.init()
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(api_browse.bp)
    app.register_blueprint(api_subscribe.bp)
    register_base_urls(app)
    return app