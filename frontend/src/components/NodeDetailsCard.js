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
  Button,
} from "@mui/material";
import Typography from "@mui/material/Typography";
import NotificationsNoneIcon from "@mui/icons-material/NotificationsNone";
import NotificationsIcon from "@mui/icons-material/Notifications";

function ValueCell(props) {
  const value = props.value;

  let cellcontent;
  if (typeof value == "object") {
    // make prettier object display if you have time
    cellcontent = JSON.stringify(value);
  } else {
    cellcontent = value;
  }

  return <TableCell align="right">{cellcontent}</TableCell>;
}

export default function NodeDetailsCard(props) {
  /* This component shows the details for a selected Node (the node description). When the selection changes,
  this component should change too. Thus it expects the selected node as a property.
  The selection should be in the state of the parent component of NodesDetailsCard.
  */
  // TODO: Let user subscribe over this card, but only if selected node is a variable.
  const [attributes, setAttributes] = useState([]);
  const [subscribed, setSubscribed] = useState(false);

  // data should be updated whenever props change...
  useEffect(() => {
    // get nodeid and namespace of the selected node
    fetch("/nodes?id=" + props.nodeid + "&ns=" + props.namespace)
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((node_attributes) => {
        console.log(node_attributes);
        setAttributes(node_attributes);
      })
      .catch((err) => console.log(err.message));
  }, [props.nodeid, props.namespace]);

  // data should be updated whenever props change...
  useEffect(() => {
    // get nodeid and namespace of the selected node
    fetch("/subscribed_nodes")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((nodes) => {
        if (nodes.includes(props.nodeid)) {
          setSubscribed(true);
        } else {
          setSubscribed(false);
        }
      })
      .catch((err) => console.log(err.message));
  }, [props.nodeid, props.namespace]);

  const subscribe = (event) => {
    fetch("/subscribe?id=" + props.nodeid + "&ns=" + props.namespace)
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setSubscribed(true);
      })
      .catch((err) => console.log(err.message));
  };

  const unsubscribe = (event) => {
    fetch("/unsubscribe?id=" + props.nodeid + "&ns=" + props.namespace)
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        setSubscribed(false);
      })
      .catch((err) => console.log(err.message));
  };

  return (
    <Card>
      <Box padding={1}>
        <Typography gutterBottom variant="h5" component="div">
          {props.nodeid == -1 ? (
            "No Node Selected"
          ) : (
            <div>{props.displayname}</div>
          )}
        </Typography>
        {subscribed ? (
          <Button onClick={unsubscribe}>
            <NotificationsIcon />
          </Button>
        ) : (
          <Button onClick={subscribe}>
            <NotificationsNoneIcon />
          </Button>
        )}

        <TableContainer>
          <Table sx={{ minWidth: 400 }} aria-lable="simple table">
            <TableHead>
              <TableRow>
                <TableCell>AttributeName</TableCell>
                <TableCell align="right">Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {attributes.map(
                (attr) =>
                  attr[1] != "" && (
                    <TableRow
                      key={attr[0]}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                    >
                      <TableCell>{attr[0]}</TableCell>
                      {attr[0] == "Value" ? (
                        <ValueCell value={attr[1]} />
                      ) : (
                        <TableCell align="right">{attr[1]}</TableCell>
                      )}
                    </TableRow>
                  )
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Card>
  );
}
