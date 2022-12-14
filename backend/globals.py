import backend.opcua_client as opcua_client
from backend.DatachangeHandler import DatachangeHandler
import backend.utils as utils

# initialize global variables

def init():
    # opcuaclient
    global uaclient
    uaclient = opcua_client.OpcuaClient()
    global subscribed_nodes
    subscribed_nodes = {}
    # update_datachage method should receive dict(nodeid, namespace, value, timestamp) as parameter and edit
    # this list
    global logging
    logging = False
    global logpath
    logpath = utils.generate_logfilename("./backend")
    #utils.create_logfile(logpath)
    def update_datachange(id, ns, timestamp, value):
        print("updating data...")
        subscribed_nodes[(id,ns)]["Value"] = value
        subscribed_nodes[(id,ns)]["Timestamp"] = timestamp
        if logging:
            utils.log(subscribed_nodes[(id,ns)])
    global handler
    handler = DatachangeHandler(update_datachange)