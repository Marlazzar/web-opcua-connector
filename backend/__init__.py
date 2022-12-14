
from flask import Flask
import backend.api_browse as api_browse
import backend.api_subscribe as api_subscribe
import backend.globals as gl
from flask import jsonify, request
import backend.utils as utils
import os

def register_base_urls(flaskapp):
    # a simple page that says hello
    @flaskapp.route('/')
    def hello():
        return "This is my flask backend" 

    @flaskapp.route('/hey')
    def hey():
        return jsonify("hello from backend")

    # catch all undefined paths
    @flaskapp.route('/', defaults={'path': ''})
    @flaskapp.route('/<path:path>')
    def catch_all(path):
        return jsonify("Backend: here is nothing"), 500


    @flaskapp.route('/connect', methods=['GET', 'POST'])
    def connect():
        gl.subscribed_nodes.clear()
        url = request.json['url']
        if request.method == 'POST':
            try:
                gl.uaclient.connect(url)
            except Exception as e:
                return jsonify("failed to connect to opcua server"), 500
        if gl.uaclient.connected:
            return jsonify("connected"), 200
        else:
            return jsonify("not connected"), 200

    @flaskapp.route('/disconnect', methods=['GET'])
    def disconnect():
        gl.uaclient.disconnect()
        return jsonify("disconnected")

    @flaskapp.route('/setlog', methods=['GET', 'POST'])
    def setlog():
        if request.method == 'POST':
            filepath = request.json['path']
            if os.path.exists(filepath):
                gl.logpath = utils.generate_logfilename(filepath)
                return jsonify("ok"), 200
            else:
                # TODO: Maybe error code?
                return jsonify("no such filepath"), 200
        else:
            return jsonify(os.path.dirname(gl.logpath)), 200
    
    @flaskapp.route('/enablelog')
    def enablelog():
        if 'switch' in request.args:
            gl.logging = not gl.logging
            return jsonify(gl.logging)
        return jsonify(gl.logging)




def create_app(test_config=None):
    gl.init()
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(api_browse.bp)
    app.register_blueprint(api_subscribe.bp)
    register_base_urls(app)
    return app