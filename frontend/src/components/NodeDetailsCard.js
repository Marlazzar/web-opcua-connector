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

export default function NodeDetailsCard(props) {
  /* This component shows the details for a selected Node (the node description). When the selection changes,
  this component should change too. Thus it expects the selected node as a property.
  The selection should be in the state of the parent component of NodesDetailsCard.
  */
  const [attributes, setAttributes] = useState([]);

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

  return (
    <Card>
      <Box padding={1}>
        <Typography gutterBottom variant="h5" component="div">
          Node Attributes
        </Typography>
        <TableContainer>
          <Table sx={{ minWidth: 400 }} aria-lable="simple table">
            <TableHead>
              <TableRow>
                <TableCell>AttributeName</TableCell>
                <TableCell align="right">Value</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {attributes.map((attr) => (
                <TableRow
                  key={attr[0]}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell>{attr[0]}</TableCell>
                  <TableCell align="right">{attr[1]}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Card>
  );
}
