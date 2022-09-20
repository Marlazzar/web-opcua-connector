import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import { TextField } from '@mui/material';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

function ConnectButton(props) {
  return (
    <Button variant="contained" onClick={props.onClick} sx={{ backgroundColor: '#0f22cc'}}>Connect</Button>
  );
}

function DisconnectButton(props) {
  return (
    <Button variant="contained" onClick={props.onClick} sx={{ backgroundColor: '#0f22cc'}}>Disconnect</Button>
  );
}


export class ConnectBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      opcua_server_url: "opc.tcp://localhost:4840/freeopcua/server/",
      connected : false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleConnect = this.handleConnect.bind(this);
    this.handleDisconnect = this.handleDisconnect.bind(this);
  }


    handleChange(event) {    this.setState({opcua_server_url: event.target.value});  }

    handleConnect(event) {
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({url: this.state.opcua_server_url})
    };
   fetch('/connect', requestOptions)
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              "http error"
            );
          }
      return response.json();
    })
    .then((acutalData) => console.log(acutalData))
    .catch((err) => console.log(err.message));
    event.preventDefault()
    this.setState({connected: true})
  }


  handleDisconnect(event) {
    fetch('/disconnect')
        .then((response) => {
          if (!response.ok) {
            throw new Error(
              "http error"
            );
          }
      return response.json();
    })
    .then((acutalData) => console.log(acutalData))
    .catch((err) => console.log(err.message));
    event.preventDefault()
    this.setState({ connected: false})
  }

  render() {
    const connected = this.state.connected
    let button;
    if (connected) {
      button = <DisconnectButton onClick={this.handleDisconnect}/>
    } else {
      button = <ConnectButton onClick={this.handleConnect}/>
    }

    return (
      <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <TextField fullWidth value={this.state.opcua_server_url} onChange={this.handleChange} />        
            </Typography>
            {button}
        </Toolbar>
      </AppBar>
      </Box>
    );
  }
}
