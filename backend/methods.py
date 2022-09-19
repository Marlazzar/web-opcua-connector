from opcua.opcua_client import UaClient


def generate_tree(root, uaclient):
    """
    This method generates the tree of nodes below the root. 
    It returns a dictionary of the following format:
    {Decription: ReferenceDescription(currentNode),
    Children: [Tree for child 1, Tree for child 2, ...]}
    """
    tree = {}
    desc = uaclient.get_node_desc(root)
    desc_dict = create_desc_dict(desc)
    tree["Description"] = desc_dict
    children = uaclient.get_children(root)
    if len(children) == 0:
        tree["Children"] = []
        return tree
    else:
        tree["Children"] = []
        for ch in children:
            new_root = uaclient.get_node(ch.NodeId)
            child_dict = generate_tree(new_root, uaclient)
            tree["Children"].append(child_dict)
        return tree
    return tree

def create_desc_dict(desc):
    desc_dict = {}
    desc_dict["DisplayName"] = str(desc.DisplayName.Text)
    desc_dict["NodeId"] = desc.NodeId.Identifier
    desc_dict["Namespace"] = desc.NodeId.NamespaceIndex
    return desc_dict

def print_tree(tree, indents=0):
    desc_dict = tree["Description"]
    displayname = desc_dict["DisplayName"]
    print("  " * indents + f"DisplayName: {displayname}")
    if len(tree["Children"]) == 0:
        print("  " * indents + "No children")
    else:
        print("  " * indents + "Children:")
        indents += 1
        for dict in tree["Children"]:
            print_tree(dict, indents=indents)

if __name__ == '__main__':
    uaclient = UaClient()
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    uaclient.connect(url)
    root = uaclient.client.nodes.root
    my_dictionary = generate_tree(root, uaclient)
    print_tree(my_dictionary)
    uaclient.disconnect()
    
