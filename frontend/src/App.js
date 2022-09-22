import "./App.css";
import React, { useEffect, useState } from "react";
import { ConnectBar } from "./components/ConnectBar";
import NodesCard from "./components/NodesCard";

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
    return (
      <div className="App">
        <ConnectBar
          connected={this.state.connected}
          onConnect={this.handleConnect}
        />
        {this.state.connected ? <NodesCard /> : "Not Connected"}
      </div>
    );
  }
}

export default App;
