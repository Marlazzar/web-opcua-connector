import backend.globals as gl
from datetime import datetime

# This method expects a ReferenceDescription of a node and
# returns a little dictionary with the most important info.
# Returns jsonify-able description.
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
def create_logfile(filename):
    f = open(filename, "w")
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
    f = open(gl.logpath, "a")
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

def generate_logfilename(filepath):
    current_time = datetime.now().strftime("%m-%d-%Y_%HUhr%M")
    filename = f"{filepath}/opcua_log_{current_time}.csv"
    return filename



