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

  handleSelect(event, selection) {
    event.preventDefault();
    this.props.onSelect(event, selection);
  }

  render() {
    return (
      <List>
        <ListItem>
          {/* Pass nodeid and namespace to state of parent component by calling handleSelect. */}
          <ListItemButton
            onClick={(e) =>
              this.handleSelect(e, {
                nodeid: this.props.nodeid,
                ns: this.props.namespace,
              })
            }
          >
            {this.props.displayname}
          </ListItemButton>
          <ListItemButton onClick={this.handleExpand} sx={{ maxWidth: 50 }}>
            {this.state.expanded ? <ExpandLess /> : <ExpandMore />}
          </ListItemButton>
        </ListItem>
        <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
          <List component="div" disablePadding sx={{ pl: 4 }}>
            {this.state.children.map((node) => (
              <Children
                namespace={node["Namespace"]}
                nodeid={node["NodeId"]}
                displayname={node["DisplayName"]}
                onSelect={this.props.onSelect}
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

  useEffect(() => {
    fetch("/children?ns=0&id=84")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error");
        }
        return response.json();
      })
      .then((acutalData) => {
        console.log(acutalData);
        setNodes(acutalData);
      })
      .catch((err) => console.log(err.message));
  }, []);

    const handleSelect = (event, selection) => {
      event.preventDefault();
      props.onSelect(event, selection);
    }

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
            <Children
              namespace={node["Namespace"]}
              nodeid={node["NodeId"]}
              displayname={node["DisplayName"]}
              onSelect={(e, selection) => handleSelect(e, selection)}
            />
          ))}
        </List>
      </Box>
    </Card>
  );
}
