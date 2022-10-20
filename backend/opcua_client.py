# initial code from https://github.com/FreeOpcUa/opcua-client-gui/blob/master/uaclient/uaclient.py
from lib2to3.pytree import Node
import logging

from asyncua import ua
from asyncua.sync import Client, SyncNode
from asyncua import crypto
from asyncua.common.ua_utils import val_to_string
from asyncua.tools import endpoint_to_strings
from asyncua.common import Node

logger = logging.getLogger(__name__)


class UaClient(object):
    """
    OPC-Ua client specialized for the need of GUI client
    return exactly what GUI needs, no customization possible
    """

    def __init__(self):
        self.application_uri = "urn:freeopcua:client-gui"
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ev = {}
        self.security_mode = None
        self.security_policy = None
        self.user_certificate_path = None
        self.user_private_key_path = None
        self.application_certificate_path = None
        self.application_private_key_path = None

    def _reset(self):
        self.client = None
        self._connected = False
        self._datachange_sub = None
        self._event_sub = None
        self._subs_dc = {}
        self._subs_ev = {}

    @staticmethod
    def get_endpoints(uri):
        client = Client(uri, timeout=2)
        edps = client.connect_and_get_server_endpoints()
        for i, ep in enumerate(edps, start=1):
            logger.info('Endpoint %s:', i)
            for (n, v) in endpoint_to_strings(ep):
                logger.info('  %s: %s', n, v)
            logger.info('')
        return edps

    def get_node(self, nodeid):
        return self.client.get_node(nodeid)

    def connect(self, uri):
        self.disconnect()
        print("connecting to %s", uri)
        logger.info("Connecting to %s with parameters %s, %s, %s, %s", uri, self.security_mode, self.security_policy,
                    self.user_certificate_path, self.user_private_key_path)
        self.client = Client(uri)
        self.client.application_uri = self.application_uri
        self.client.description = "FreeOpcUa Client GUI"

        # Set user identity token
        if self.user_private_key_path:
            self.client.load_private_key(self.user_private_key_path)
        if self.user_certificate_path:
            self.client.load_client_certificate(self.user_certificate_path)

        # Set security mode and security policy
        if self.security_mode is not None and self.security_policy is not None:
            self.client.set_security(
                getattr(crypto.security_policies, 'SecurityPolicy' + self.security_policy),
                self.application_certificate_path,
                self.application_private_key_path,
                mode=getattr(ua.MessageSecurityMode, self.security_mode)
            )
        self.client.connect()
        self._connected = True
        self.client.load_data_type_definitions()
        try:
            self.client.load_enums()
            self.client.load_type_definitions()
        except Exception:
            logger.exception("Loading custom stuff with spec <= 1.03 did not work")

    def disconnect(self):
        if self._connected:
            print("Disconnecting from server")
            self._connected = False
            try:
                self.client.disconnect()
            finally:
                self._reset()

    def subscribe_datachange(self, node, handler):
        if not self._datachange_sub:
            self._datachange_sub = self.client.create_subscription(500, handler)
        handle = self._datachange_sub.subscribe_data_change(node)
        self._subs_dc[node.nodeid] = handle
        return handle

    def unsubscribe_datachange(self, node):
        self._datachange_sub.unsubscribe(self._subs_dc[node.nodeid])

    def subscribe_events(self, node, handler):
        if not self._event_sub:
            print("subscirbing with handler: ", handler, dir(handler))
            self._event_sub = self.client.create_subscription(500, handler)
        handle = self._event_sub.subscribe_events(node)
        self._subs_ev[node.nodeid] = handle
        return handle

    def unsubscribe_events(self, node):
        self._event_sub.unsubscribe(self._subs_ev[node.nodeid])

    def get_node_attrs(self, node):
        if not isinstance(node, SyncNode):
            node = self.client.get_node(node)
        attrs = node.read_attributes([ua.AttributeIds.DisplayName, ua.AttributeIds.BrowseName, ua.AttributeIds.NodeId])
        return node, [attr.Value.Value.to_string() for attr in attrs]

    @staticmethod
    def get_children(node):
        descs = node.get_children_descriptions()
        descs.sort(key=lambda x: x.BrowseName)
        return descs

    @staticmethod
    def get_node_desc(node):
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

    # from FreeOpcUas' opcua-widgets/attrs_widget.py
    def get_all_attributes(self, node, all=True, attributes=[]):
        # default behaviour: send all the attributes in a list
        # if all=False: send only attributes specified in attributes parameter
        if all:
            attrs = [attr for attr in ua.AttributeIds]
        else:
            attrs = attributes
        dvs = node.read_attributes(attrs)
        # get list of (attributename, datavalue)
        res = []
        for idx, dv in enumerate(dvs):
            if dv.StatusCode.is_good():
                res.append((attrs[idx], dv))
        final_results = []
        # try to get the datavalues in a readable string
        for attr, dv in res:
            try:
                # is the attribute a value?
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
                        string = enum_to_string(attr, dv.Value.Value)
                    elif isinstance(dv.Value.Value, ua.LocalizedText):
                        string = dv.Value.Value.Text
                    elif attr == ua.AttributeIds.DataType:
                        # opcua uses nodes to define datatypes. The displayname of the node is the
                        # name of the datatype. The attribute DataType holds a NodeId Object referencing
                        # the dataype node.
                        node = self.get_node(dv.Value.Value)
                        string = node.read_attribute(ua.AttributeIds.DisplayName).Value.Value.Text
                    else:
                        string = val_to_string(dv.Value.Value)
                    attr_name = attr.name
                    value = string
                    final_results.append((attr_name, value))
            except Exception as ex:
                logger.exception(f"Exception while displaying attribute {attr} with value {dv} for node {node}")
        return final_results


def attr_to_enum(attr):
    attr_name = attr.name
    if attr_name.startswith("User"):
        attr_name = attr_name[4:]
    return getattr(ua, attr_name)


def enum_to_string(attr, val):
    attr_enum = attr_to_enum(attr)
    string = ", ".join([e.name for e in attr_enum.parse_bitfield(val)])
    return string
        

if __name__ == '__main__':
    uaclient = UaClient()
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    uaclient.connect(url)
    node = uaclient.get_node("ns=0;i=7597")
    attributes = uaclient.get_all_attributes(node)
    print(attributes)
    for tuple in attributes:
        if tuple[0] == 'Value':
            print(type(tuple[1][0]))
    uaclient.disconnect()
    print("disconnected")