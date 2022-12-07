from asyncua import ua
from asyncua.sync import Client, SyncNode
from asyncua import crypto
from asyncua.common.ua_utils import val_to_string
from asyncua.tools import endpoint_to_strings
import logging

logger = logging.getLogger(__name__)


class OpcuaClient():
    def __init__(self):
        self.application_uri = "urn:opcua:client-wrapper"
        self.client = None
        self.connected = False
        self.subscription = None
        self.sub_description = {}

    def connect(self, uri):
        self.disconnect()
        print(f"client connecting to {uri}")
        self.client = Client(uri)
        self.client.application_uri = self.application_uri
        self.client.description = "Opcua Client"

        self.client.connect()
        self.connected = True

    def disconnect(self):
        if self.connected:
            print("disconnect")
            self.connected = False
            try:
                self.client.disconnect()
            finally:
                self.connected = False
                self.client = None
                self.sub_description = {}
            
    def subscribe_datachange(self, node, handler):
        if not self.subscription:
            self.subscription = self.client.create_subscription(500, handler)
        handle = self.subscription.subscribe_data_change(node)
        self.sub_description[node.nodeid] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self.subscription.unsubscribe(self.sub_description[node.nodeid])

    def get_node(self, nodeid):
        return self.client.get_node(nodeid)

    def get_node_attrs(self, node):
        if not isinstance(node, SyncNode):
            node = self.client.get_node(node)
        attrs = node.read_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
        return node, [attr.Value.Value.to_string() for attr in attrs]

    def get_children(self, node):
        descs = node.get_children_descriptions()
        descs.sort(key=lambda x: x.BrowseName)
        return descs

    def get_node_desc(self, node):
        attrs = node.read_attributes(
            [ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId
             , ua.AttributeIds.NodeClass])
        desc = ua.ReferenceDescription()
        desc.DisplayName = attrs[0].Value.Value
        desc.BrowseName = attrs[1].Value.Value
        desc.NodeId = attrs[2].Value.Value
        desc.NodeClass = attrs[3].Value.Value
        desc.TypeDefinition = ua.TwoByteNodeId(ua.ObjectIds.FolderType)
        return desc

    def get_all_attributes(self, node, all=True, attributes=[]):
        # default behaviour: send all the attributes in a list
        # if all=False: send only attributes specified in attributes parameter
        if all:
            attributes = [attr for attr in ua.AttributeIds]
        datavalues = node.read_attributes(attributes)
        # get list of (attributename, datavalue)
        res = []
        for idx, dv in enumerate(datavalues):
            if dv.StatusCode.is_good():
                res.append((attributes[idx], dv))
        final_results = []
        # try to parse the datavalues into a readable string
        for attr, dv in res:
            try:
                # is the attribute of type value?
                if attr == ua.AttributeIds.Value:
                    name = "Value"
                    # Note: value_obj can contain pretty complicated structures, like nested lists and dicts
                    value_obj = dv.Value.Value
                    final_results.append((name, value_obj))
                else:
                    if attr in (ua.AttributeIds.AccessLevel,
                      ua.AttributeIds.UserAccessLevel,
                      ua.AttributeIds.WriteMask,
                      ua.AttributeIds.UserWriteMask,
                      ua.AttributeIds.EventNotifier):
                        dv_string = attr_to_string(attr, dv.Value.Value)
                    elif isinstance(dv.Value.Value, ua.LocalizedText):
                        dv_string = dv.Value.Value.Text
                    elif attr == ua.AttributeIds.DataType:
                        # opcua uses nodes to define datatypes. The displayname of the node is the
                        # name of the datatype. The attribute DataType holds a NodeId Object referencing
                        # the dataype node.
                        node = self.get_node(dv.Value.Value)
                        dv_string = node.read_attribute(ua.AttributeIds.DisplayName).Value.Value.Text
                    elif attr == ua.AttributeIds.NodeClass:
                        dv_string = str(ua.NodeClass(dv.Value.Value))
                    else:
                        dv_string = val_to_string(dv.Value.Value)
                    attr_name = attr.name
                    value = dv_string
                    final_results.append((attr_name, value))
            except Exception as ex:
                logger.exception(f"Exception while displaying attribute {attr} with value {dv} for node {node}")
        return final_results

    def read_display_name(self, node):
        displayname = node.read_attribute(ua.AttributeIds.DisplayName).Value.Value.Text
        return displayname
    
    def read_datatype(self, node):
        datatypenode = self.get_node(node.read_attribute(ua.AttributeIds.DataType).Value.Value)
        datatype = self.read_display_name(datatypenode)
        return datatype

def attr_to_string(attr, val):
    attr_name = attr.name
    # cut off unnecessary infos
    if attr_name.startswith("User"):
        attr_name = attr_name[4:]
    tmp = getattr(ua, attr_name)
    string = ", ".join([e.name for e in tmp.parse_bitfield(val)])
    return string
        

