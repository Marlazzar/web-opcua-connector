import backend.opcua_client as opcua_client
from backend.DatachangeHandler import DatachangeHandler
import backend.utils as utils
# initialize global variables


def init():
    # opcuaclient
    global uaclient
    uaclient = opcua_client.UaClient()
    global subscribed_nodes
    subscribed_nodes = {}
    # update_datachage method should receive dict(nodeid, namespace, value, timestamp) as parameter and edit
    # this list
    global logging
    logging = True
    global logfile
    logfile = "./backend/log.txt"
    utils.create_logfile(logfile)
    def update_datachange(nodedict):
        print("updating data...")
        # called once even for const
        # TODO: This needs to log
        id = nodedict["NodeId"]
        ns = nodedict["Namespace"]
        subscribed_nodes[(id,ns)] = nodedict
        if logging:
            utils.log(nodedict)
    global handler
    handler = DatachangeHandler(update_datachange)

