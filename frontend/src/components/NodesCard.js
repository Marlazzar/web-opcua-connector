import * as React from "react";
import Card from "@mui/material/Card";
import Typography from "@mui/material/Typography";
import { useState, useEffect } from "react";
import {
  List,
  ListSubheader,
  CardHeader,
  Box,
  ListItemButton,
  ListItem,
  ListItemText,
  Collapse,
} from "@mui/material";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";

class Children extends React.Component {
  constructor(props) {
    super(props);
    this.state = { children: [], expanded: false, fetched: false };
    this.handleExpand = this.handleExpand.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
  }

  handleExpand(event) {
    event.preventDefault();
    this.setState((state) => ({ expanded: !state.expanded }));

    if (!this.state.fetched) {
      fetch("/children?ns=" + this.props.namespace + "&id=" + this.props.nodeid)
        .then((response) => {
          if (!response.ok) {
            throw new Error("http error");
          }
          return response.json();
        })
        .then((acutalData) => {
          console.log(acutalData);
          this.setState({ children: acutalData, fetched: true });
        })
        .catch((err) => console.log(err.message));
    }
  }

  // tell parentComponent (NodesCard) the new selection
  handleSelect(event, selection) {
    event.preventDefault();
    this.props.onSelect(event, selection);
  }

  render() {
    const isSelected = this.props.nodeid == this.props.selection.nodeid;

    return (
      <List>
        <ListItem>
          {/* Check whether the current node is the selected node */}
          <ListItemButton
            onClick={(e) =>
              this.handleSelect(e, {
                nodeid: this.props.nodeid,
                ns: this.props.namespace,
                displayname: this.props.displayname,
                nodeclass: this.props.nodeclass,
              })
            }
            selected={isSelected}
          >
            <Typography>{this.props.displayname}</Typography>
          </ListItemButton>
          <ListItemButton onClick={this.handleExpand} sx={{ maxWidth: 50 }}>
            {this.state.expanded ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
        </ListItem>
        <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
          <List component="div" disablePadding sx={{ pl: 4 }}>
            {/* Click button, to show children of clicked node - like this, we can browse through the entire node tree. */}
            {this.state.children.map((node) => (
              <Children
                namespace={node["Namespace"]}
                nodeid={node["NodeId"]}
                displayname={node["DisplayName"]}
                nodeclass={node["Nodeclass"]}
                onSelect={this.props.onSelect}
                selection={this.props.selection}
              />
            ))}
          </List>
        </Collapse>
      </List>
    );
  }
}

export default function NodesCard(props) {
  const [nodes, setNodes] = useState([]);
  const [selection, setSelection] = useState({
    nodeid: -1,
    ns: -1,
    displayname: "",
    nodeclass: -1,
  });

  useEffect(() => {
    // get nodeid and namespace of root
    fetch("/root")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error: root not found");
        }
        return response.json();
      })
      .then((root) => {
        console.log(root);
        const id = root.NodeId;
        const ns = root.Namespace;
        fetch("/children?ns=" + ns + "&id=" + id)
          .then((response) => {
            if (!response.ok) {
              throw new Error("http error: children of root not found");
            }
            return response.json();
          })
          .then((acutalData) => {
            console.log(acutalData);
            setNodes(acutalData);
          })
          .catch((err) => console.log(err.message));
      });
  }, []);

  // tell parent component (App) the new selection
  const handleSelect = (event, selection) => {
    event.preventDefault();
    props.onSelect(event, selection);
    setSelection(selection);
  };

  return (
    <Card sx={{ minWidth: 300 }}>
      <Box padding={1}>
        <Typography gutterBottom variant="h5" component="div">
          Nodes
        </Typography>
        <List
          sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
        >
          {nodes.map((node) => (
            // selection needs to be managed by NodesCard, because only one selection
            // for the entire NodesCard is possible.
            <Children
              namespace={node["Namespace"]}
              nodeid={node["NodeId"]}
              displayname={node["DisplayName"]}
              nodeclass={node["Nodeclass"]}
              onSelect={(e, selection) => handleSelect(e, selection)}
              selection={selection}
            />
          ))}
        </List>
      </Box>
    </Card>
  );
}
