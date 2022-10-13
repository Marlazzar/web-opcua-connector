from asyncua import ua

# This method expects a ReferenceDescription of a node and
# returns a little dictionary with the most important info.
def create_desc_dict(desc):
    desc_dict = {}
    desc_dict["DisplayName"] = str(desc.DisplayName.Text)
    desc_dict["NodeId"] = desc.NodeId.Identifier
    desc_dict["Namespace"] = desc.NodeId.NamespaceIndex
    desc_dict["NodeClass"] = str(ua.NodeClass(desc.NodeId.NodeIdType))
    return desc_dict

def dict_keys_list(dict):
    mylist = []
    for k in dict.keys():
        mylist.append(k[0])
    return mylist
