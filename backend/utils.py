from asyncua import ua
import backend.globals as gl

# This method expects a ReferenceDescription of a node and
# returns a little dictionary with the most important info.
def create_desc_dict(desc):
    desc_dict = {}
    desc_dict["DisplayName"] = str(desc.DisplayName.Text)
    desc_dict["NodeId"] = desc.NodeId.Identifier
    desc_dict["Namespace"] = desc.NodeId.NamespaceIndex
    desc_dict["NodeClass"] = desc.NodeClass_
    return desc_dict

def dict_keys_list(dict):
    mylist = []
    for k in dict.keys():
        mylist.append(k[0])
    return mylist


### methods for logging ###
def create_logfile(logfile):
    f = open(logfile, "w")
    f.write("Timestamp, DisplayName, DataType, Value\n")
    f.close()

def log(nodedict):
    # TODO: log displayname, datatype, timestamp, value to single logfile
    # logline should look like this: 
    # timestamp:<time>, displayname:<dname>, datatype:<dtype>, value:<value>
    print("logging...")
    timestamp = nodedict["Timestamp"]
    displayname = nodedict["Displayname"]
    datatype = nodedict["Datatype"]
    value = nodedict["Value"]
    logline = f"{timestamp}, {displayname}, {datatype}, {value}"
    f = open(gl.logfile, "a")
    f.write(logline + "\n")
    f.close()

# to make sure all the dicts in subscribed_nodes have the same keys, please use this method
# to generate a proper dict
def create_nodedict(id, ns, timestamp, displayname, datatype, value):
    nodedict = {}
    nodedict["NodeId"] = id
    nodedict["Namespace"] = ns
    nodedict["Timestamp"] = timestamp
    nodedict["Displayname"] = displayname
    nodedict["Datatype"] = datatype
    nodedict["Value"] = value
    return nodedict



