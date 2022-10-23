import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import { TextField } from "@mui/material";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

function ConnectButton(props) {
  return (
    <Button
      variant="contained"
      onClick={props.onClick}
      sx={{ backgroundColor: "#0f22cc" }}
    >
      Connect
    </Button>
  );
}

function DisconnectButton(props) {
  return (
    <Button
      variant="contained"
      onClick={props.onClick}
      sx={{ backgroundColor: "#0f22cc" }}
    >
      Disconnect
    </Button>
  );
}

export class ConnectBar extends React.Component {
  /* This component shows a Textfield where the user can specify the url of
  the opcua server. 
  Property: 
  onConnect: method that will be called, when the user clicks "connect"
  connected: boolean. true, if already connected to a opcua server.
  */
  constructor(props) {
    super(props);
    this.state = {
      opcua_server_url: "opc.tcp://opcua_server:4840/",
      data: [],
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleConnect = this.handleConnect.bind(this);
    this.handleDisconnect = this.handleDisconnect.bind(this);
  }

  handleChange(event) {
    this.setState({ opcua_server_url: event.target.value });
  }

  handleConnect(event) {
    event.preventDefault();
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: this.state.opcua_server_url }),
    };
    fetch("/connect", requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Http error " + response.status);
        }
        return response.json();
      })
      .then((acutalData) => {
        console.log(acutalData);
        this.setState({ data: acutalData });
        if (acutalData == "connected") {
          this.props.onConnect(event);
        }
      })
      .catch((err) => console.log(err.message));
  }

  handleDisconnect(event) {
    event.preventDefault();
    fetch("/disconnect")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error");
        }
        return response.json();
      })
      .then((acutalData) => console.log(acutalData))
      .catch((err) => console.log(err.message));
    this.props.onConnect(event);
  }

  render() {
    const connected = this.props.connected;
    let button;
    if (connected) {
      button = <DisconnectButton onClick={this.handleDisconnect} />;
    } else {
      button = <ConnectButton onClick={this.handleConnect} />;
    }

    return (
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              <TextField
                fullWidth
                value={this.state.opcua_server_url}
                onChange={this.handleChange}
              />
            </Typography>
            {button}
          </Toolbar>
        </AppBar>
      </Box>
    );
  }
}
