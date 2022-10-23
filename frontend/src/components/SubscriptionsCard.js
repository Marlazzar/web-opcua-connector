import * as React from "react";
import { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import {
  Card,
  TableHead,
  TableRow,
  Table,
  TableBody,
  TableCell,
  TableContainer,
} from "@mui/material";
import Typography from "@mui/material/Typography";

function SubscriptionRow(props) {
  const [nodedict, setNodedict] = useState({});

  useEffect(() => {
    fetch("/get_sub?id=" + props.nodeid + "&ns=2")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error subscribe " + response.status);
        }
        return response.json();
      })
      .then((newnodedict) => {
        console.log(newnodedict);
        setNodedict(newnodedict);
      })
      .catch((err) => console.log(err.message));
  });

  return (
    <TableRow>
      <TableCell>{nodedict["NodeId"]}</TableCell>
      <TableCell>{nodedict["Value"]}</TableCell>
      <TableCell>{nodedict["Timestamp"]}</TableCell>
    </TableRow>
  );
}

export default function SubscriptionsCard() {
  const [subscriptednodes, setSubscriptednodes] = useState([]);

  // data should be updated whenever props change...
  useEffect(() => {
    // get nodeid and namespace of the selected node
    fetch("/subscripted_nodes")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((nodes) => {
        setSubscriptednodes(nodes);
      })
      .catch((err) => console.log(err.message));
  }, []);
  return (
    <Card>
      <Box padding={1}>
        <Typography gutterBottom variant="h5" component="div">
          Subscriptions
        </Typography>
        <TableContainer>
          <Table sx={{ minWidth: 800 }} aria-lable="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Nodeid</TableCell>
                <TableCell>Value</TableCell>
                <TableCell align="right">Timestamp</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {subscriptednodes.map((node) => (
                <SubscriptionRow nodeid={node} />
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Card>
  );
}
