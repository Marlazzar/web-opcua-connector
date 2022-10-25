import React, { useEffect, useState } from "react";
import NodesCard from "./NodesCard";
import NodesDetailsCard from "./NodeDetailsCard";
import SubscriptionsCard from "./SubscriptionsCard";
import { Container, Grid, Stack } from "@mui/material";
import { width } from "@mui/system";

class ContentGridGard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      connected: false,
      selectedNode: { nodeid: -1, ns: -1, displayname: "", nodeclass: -1 },
    };
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
      <Container sx={{ p: 2 }}>
        <Grid container sx={{ flexGrow: 1 }}>
          <Grid item xs={12} justifyContent="center">
            <Grid container spacing={2} direction="row">
              <Grid item xs={6}>
                <NodesCard
                  onSelect={(e, selection) => this.handleSelect(e, selection)}
                  sx={{ height: "100%" }}
                />
              </Grid>
              <Grid item xs={6}>
                <NodesDetailsCard
                  nodeid={this.state.selectedNode.nodeid}
                  namespace={this.state.selectedNode.ns}
                  displayname={this.state.selectedNode.displayname}
                  sx={{ height: "100%" }}
                />
              </Grid>
            </Grid>
            <Grid item xs={12}>
              <SubscriptionsCard />
            </Grid>
          </Grid>
        </Grid>
      </Container>
    );
  }
}

export default ContentGridGard;
