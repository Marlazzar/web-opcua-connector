import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import DialogTitle from "@mui/material/DialogTitle";
import Dialog from "@mui/material/Dialog";
import {
  TextField,
  Stack,
  Avatar,
  ListItemAvatar,
  FormGroup,
  FormControlLabel,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import CloseIcon from "@mui/icons-material/Close";
import Switch from "@mui/material/Switch";

function LoggingDialog(props) {
  const { open, onClose, onEnablelog, defaultlog } = props;
  const [selection, setSelection] = React.useState("");

  useEffect(() => {
    fetch("/setlog")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        setSelection(data);
      })
      .catch((err) => console.log(err.message));
  }, []);

  const handleClose = () => {
    onClose();
  };

  const handleUpdate = (value) => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: selection }),
    };
    fetch("/setlog", requestOptions)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Http error " + response.status);
        }
        return response.json();
      })
      .then((acutalData) => {
        if (acutalData == "ok") {
          console.log("updated log file: " + selection);
        } else {
          setSelection("Error");
          console.log("Failed changing log file in backend");
          console.log(acutalData);
        }
      })
      .catch((er) => {
        console.log(er.message);
      });
    handleClose();
  };

  const handleSwitch = () => {
    fetch("/enablelog?switch")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((data) => {
        onEnablelog(data);
        console.log("enablelog set to " + data);
      })
      .catch((er) => console.log(er.message));
  };

  return (
    <Dialog onClose={handleClose} open={open}>
      <DialogTitle>Set path to logfile</DialogTitle>
      <FormGroup sx={{ px: 1 }}>
        <FormControlLabel
          control={
            <Switch
              sx={{ m: 1 }}
              onChange={handleSwitch}
              defaultChecked={defaultlog}
            />
          }
          label="Enable logging"
        />
      </FormGroup>
      <List sx={{ pt: 0 }}>
        <ListItem>
          <TextField
            onChange={(event) => setSelection(event.target.value)}
            defaultValue={selection}
          >
            Enter logfilepath
          </TextField>
        </ListItem>
        <ListItem autoFocus button onClick={handleUpdate}>
          <ListItemAvatar>
            <Avatar>
              <EditIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="change logpath" />
        </ListItem>
        <ListItem autoFocus button onClick={handleClose}>
          <ListItemAvatar>
            <Avatar>
              <CloseIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="close" />
        </ListItem>
      </List>
    </Dialog>
  );
}

LoggingDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  selectedValue: PropTypes.string.isRequired,
};

export default function OpenLogDialog() {
  const [open, setOpen] = React.useState(false);
  const [hasError, setError] = React.useState(false);
  const [enablelog, setEnablelog] = React.useState(false);

  useEffect(() => {
    // enablelog is only fetched once, so if somebody else changes the value in the backend
    // the switch might be ought of sync.
    fetch("/enablelog")
      .then((response) => {
        if (!response.ok) {
          throw new Error("http error " + response.status);
        }
        return response.json();
      })
      .then((enlogdata) => {
        setEnablelog(enlogdata);
      })
      .catch((err) => console.log(err.message));
  }, []);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleEnablelog = () => {
    const newvalue = !enablelog;
    setEnablelog(newvalue);
  };

  return (
    <Stack direction="row" spacing={2}>
      <Button variant="outlined" onClick={handleClickOpen} size="small">
        logs
      </Button>
      <LoggingDialog
        open={open}
        onClose={handleClose}
        onEnablelog={handleEnablelog}
        defaultlog={enablelog}
      />
    </Stack>
  );
}
