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

  render() {
    return (
      <List>
        <ListItemButton id={this.props.nodeid} onClick={this.handleExpand}>
          <ListItemText primary={this.props.displayname} />
          {this.state.expanded ? <ExpandLess /> : <ExpandMore />}
        </ListItemButton>
        <Collapse in={this.state.expanded} timeout="auto" unmountOnExit>
          <List component="div" disablePadding sx={{ pl: 4 }}>
            {this.state.children.map((node) => (
              <Children
                namespace={node["Namespace"]}
                nodeid={node["NodeId"]}
                displayname={node["DisplayName"]}
              />
            ))}
          </List>
        </Collapse>
      </List>
    );
  }
}

export default function NodesCard() {
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

  return (
    <Card>
      <CardHeader>
        <Typography gutterBottom variant="h5" component="div">
          Nodes
        </Typography>
      </CardHeader>
      <Box padding={1}>
        <List
          sx={{ width: "100%", maxWidth: 360, bgcolor: "background.paper" }}
          component="nav"
          aria-labelledby="nested-list-subheader"
          subheader={
            <ListSubheader component="div" id="nested-list-subheader">
              Nodes
            </ListSubheader>
          }
        >
          {nodes.map((node) => (
            <Children
              namespace={node["Namespace"]}
              nodeid={node["NodeId"]}
              displayname={node["DisplayName"]}
            />
          ))}
        </List>
      </Box>
    </Card>
  );
}
