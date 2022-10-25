import "./App.css";
import React, { useEffect, useState } from "react";
import { ConnectBar } from "./components/ConnectBar";
import ContentGridGard from "./components/ContentGridCard";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      connected: false,
      selectedNode: { nodeid: -1, ns: -1, displayname: "", nodeclass: -1 },
    };
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
    return (
      <div className="App">
        <ConnectBar
          connected={this.state.connected}
          onConnect={this.handleConnect}
        />
        {this.state.connected && <ContentGridGard />}
      </div>
    );
  }
}

export default App;
