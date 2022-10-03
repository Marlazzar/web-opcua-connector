import "./App.css";
import React, { useEffect, useState } from "react";
import { ConnectBar } from "./components/ConnectBar";
import NodesCard from "./components/NodesCard";
import NodesDetailsCard from "./components/NodeDetailsCard"
import { Stack, Item } from "@mui/material"

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { connected: false };
    this.handleConnect = this.handleConnect.bind(this);
  }

  handleConnect(event) {
    event.preventDefault();
    this.setState((state) => ({ connected: !state.connected }));
  }

  render() {
    let content;
    if (this.state.connected) {
      content = <Stack direction="row" spacing={2} padding={2}>
        <NodesCard/>
      <NodesDetailsCard nodeid={84} namespace={0} selected={true}/>
      </Stack>;
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
