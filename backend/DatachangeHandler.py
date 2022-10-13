import sys
import asyncua
from itsdangerous import BadTimeSignature
sys.path.insert(0,'..')
from opcua.opcua_client import UaClient
import asyncua.ua.uaerrors as uaerrors
from datetime import datetime

class DatachangeHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def __init__(self, callback):
        super()
        self.callback = callback

    def datachange_notification(self, node, val, data):
        # instead of just printing this, we need to send it to the frontend somehow
        # right now, any node can change this val, you won't know what node it belongs to....
        # This should fire a event, that notifies listeners for THIS node
        if data.monitored_item.Value.SourceTimestamp:
            dato = data.monitored_item.Value.SourceTimestamp.isoformat()
        elif data.monitored_item.Value.ServerTimestamp:
            dato = data.monitored_item.Value.ServerTimestamp.isoformat()
        else:
            dato = datetime.now().isoformat()
        # fire event
        nodedict = {}
        nodedict["NodeId"] = node.nodeid.Identifier
        nodedict["Namespace"] = node.nodeid.NamespaceIndex
        nodedict["Value"] = str(val)
        nodedict["Timestamp"] = dato
        self.callback(nodedict)



    def event_notification(self, event):
        print("New event", event)

