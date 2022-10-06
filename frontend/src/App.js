import "./App.css";
import React, { useEffect, useState } from "react";
import { ConnectBar } from "./components/ConnectBar";
import NodesCard from "./components/NodesCard";
import NodesDetailsCard from "./components/NodeDetailsCard";
import { Stack, Item } from "@mui/material";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { connected: false, selectedNode: { nodeid: -1, ns: -1 } };
    this.handleConnect = this.handleConnect.bind(this);
    this.handleSelect = this.handleSelect.bind(this);
  }

  handleConnect(event) {
    event.preventDefault();
    this.setState((state) => ({ connected: !state.connected }));
  }

  handleSelect(event, selection) {
    event.preventDefault();
    console.log(
      "selected node: id=" + selection["nodeid"] + ";ns=" + selection["ns"]
    );
    this.setState({ selectedNode: selection });
  }

  render() {
    let content;
    if (this.state.connected) {
      content = (
        <Stack direction="row" spacing={2} padding={2}>
          <NodesCard
            onSelect={(e, selection) => this.handleSelect(e, selection)}
          />
          <NodesDetailsCard
            nodeid={this.state.selectedNode.nodeid}
            namespace={this.state.selectedNode.ns}
          />
        </Stack>
      );
    } else {
      content = <p>Not Connected</p>;
    }
    return (
      <div className="App">
        <ConnectBar
          connected={this.state.connected}
          onConnect={this.handleConnect}
        />
        {content}
      </div>
    );
  }
}

export default App;
