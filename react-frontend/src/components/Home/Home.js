import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import * as forge from 'node-forge';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { Alert, Button } from "@mui/material";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import Snackbar from "@mui/material/Snackbar";
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close'; 
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';


export default function Home() {
  const dispatch = useDispatch();
  const [rsaKey, setRsaKey] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [hosts, setHosts] = useState(useSelector((state) => state.hosts.hosts));
  const [tags, setTags] = useState(useSelector((state) => state.tags.tags));
  const [selectedTags, setSelectedTags] = useState(useSelector((state) => state.selectedTags.selectedTags));
  const [backdropOpen, setBackdropOpen] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState("");
  const [messageColor, setMessageColor] = useState("success");
  const [dialogOpen, setDialogOpen] = useState(false);
  const [dialogMessage, setDialogMessage] = useState("");


  const fetchTags = async () => {
    const install_response = await fetch(process.env.REACT_APP_API_URL + "/install/tags");
    const install_data = await install_response.json();
    const uninstall_response = await fetch(process.env.REACT_APP_API_URL + "/uninstall/tags");
    const uninstall_data = await uninstall_response.json();
    const data = [...install_data]
    for (let i = 0; i < uninstall_data.length; i++) {
      if (!data.some((item) => item.title === uninstall_data[i]["title"])) {
        uninstall_data[i]["title"] = uninstall_data[i]["title"] + " (uninstall only)";
        data.push(uninstall_data[i]);
      }
    }
    for (let i = 0; i < install_data.length; i++) {
      if (!uninstall_data.some((item) => item.title === install_data[i]["title"])) {
        data.splice(i, 1);
        install_data[i]["title"] = install_data[i]["title"] + " (install only)";
        data.push(install_data[i]);
      }
    }
    setTags(data);
    dispatch({ type: "tags/setTags", payload: data });
  };

  const fetchRSAKey = async () => {
    const response = await fetch(process.env.REACT_APP_API_URL + "/public_key");
    const data = await response.json();
    setRsaKey(data["public_key"]);
  };

  useEffect(() => {
    fetchTags();
    fetchRSAKey();
  }, []);

  useEffect(() => {
    dispatch({ type: "currentPage/setCurrentPage", payload: "Installer" });
  }, []);

  const descriptionElementRef = React.useRef(null);
  React.useEffect(() => {
    if (dialogOpen) {
      const { current: descriptionElement } = descriptionElementRef;
      if (descriptionElement !== null) {
        descriptionElement.focus();
      }
    }
  }, [dialogOpen]);

  if (rsaKey === "") {
    return (
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={true}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  }

  const handleSoftwareListChange = (value) => {
    var tagsList = [];
    value.map((softwareItem) => {
      softwareItem.tags.map((tag) => {
        if (!tagsList.includes(tag)) {
          tagsList.push(tag);
        }
      });
    });
    setSelectedTags(tagsList);
    dispatch({ type: "selectedTags/setSelectedTags", payload: tagsList });
  };

  const handleHostsChange = (value) => {
    setHosts(value);
    dispatch({ type: "hosts/setHosts", payload: value });
  };
  if (rsaKey !== "") {
    var publicKey = forge.pki.publicKeyFromPem(rsaKey);
  }
  else {
    publicKey = "";
  }
  var encrypt = function (text) {
    let encrypted = publicKey.encrypt(text, "RSA-OAEP", {
      md: forge.md.sha256.create(),
      mgf1: {
        md: forge.md.sha256.create(),
      },
    });
    return forge.util.encode64(encrypted);
  };

  const handlePing = () => {
    setBackdropOpen(true);
    const encryptedUsername = encrypt(username);
    const encryptedPassword = encrypt(password);
    const encryptedHosts = encrypt(hosts);

    fetch(process.env.REACT_APP_API_URL + "/target/ping", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        hosts: encryptedHosts,
        user: encryptedUsername,
        password: encryptedPassword,
      }),
    })
    .then((response) => {
      return [response.json(), response.ok];
    })
    .then(async (data) => {
      var status = data[1];
      data = await data[0];
      if (!status) {
        throw new Error(data.detail);
      }
      console.log("Success:",data);
      setSnackbarOpen(true);
      setSnackbarMessage("Ping successful");
      setBackdropOpen(false);
      setMessageColor("success");
      setDialogMessage(data);
    })
    .catch((error) => {
      console.log(error);
      setSnackbarOpen(true);
      setSnackbarMessage("Ping failed");
      setBackdropOpen(false);
      setMessageColor("error");
      setDialogMessage(error.message);
    });
  };

  const handleInstallUninstall = (install) => {
    setBackdropOpen(true);
    const encryptedUsername = encrypt.encrypt(username.encode());
    const encryptedPassword = encrypt.encrypt(password.encode());
    const encryptedHosts = encrypt.encrypt(hosts.encode());

    const api_url = install?"/target/install":"/target/uninstall";
    fetch(process.env.REACT_APP_API_URL + api_url, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        hosts: encryptedHosts,
        user: encryptedUsername,
        password: encryptedPassword,
        tags: selectedTags,
      }),
    })
    .then((response) => {
      return [response.json(), response.ok];
    })
    .then(async (data) => {
      var status = data[1];
      data = await data[0];
      if (!status) {
        throw new Error(data.detail);
      }
      console.log("Success:",data);
      setSnackbarOpen(true);
      setSnackbarMessage("Install successful");
      setBackdropOpen(false);
      setMessageColor("success");
      setDialogMessage(data);
    })
    .catch((error) => {
      console.log(error);
      setSnackbarOpen(true);
      setSnackbarMessage("Install failed");
      setBackdropOpen(false);
      setMessageColor("error");
      setDialogMessage(error.message);
    });
  };

  const snackbaraction = (
    <React.Fragment>
      <Button color="secondary" size="small" onClick={() => {setDialogOpen(true);}}>
        View Details
      </Button>
      <IconButton
        size="small"
        aria-label="close"
        color="inherit"
        onClick={() => {setSnackbarOpen(false);}}
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </React.Fragment>
  );

  return (
    <div>
      <h1>Quick Installer</h1>
      <p>Page for installing and uninstalling software on multiple hosts with minimal configuration</p>
      <Grid container spacing={4} padding={4}>
        <Grid item xs={12} md={6}>
          <TextField
            id="username"
            required
            label="Username"
            variant="filled"
            fullWidth
            onChange={(event) => {setUsername(event.target.value);}}
            value={username}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            id="password"
            required
            label="Password"
            type="password"
            variant="filled"
            fullWidth
            onChange={(event) => {setPassword(event.target.value);}}
            value={password}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="hosts"
            required
            label="Hosts"
            variant="filled"
            fullWidth
            placeholder="IP addresses or hostnames separated by commas"
            onChange={(event) => {handleHostsChange(event.target.value);}}
            value={hosts}
          />
        </Grid>
        <Grid item xs={12}>
          <Autocomplete
              multiple
              id="tags-outlined"
              options={tags}
              getOptionLabel={(option) => option.title}
              filterSelectedOptions
              renderInput={(params) => (
              <TextField
                  {...params}
                  label="Select Software"
                  placeholder="Select Software"
              />
              )}
              onChange={(event, value) => {handleSoftwareListChange(value);}}
          />
        </Grid>
        <Grid item container>
          <Grid item margin={2} marginLeft={0}>
            <Button variant="outlined" onClick={() => {handleInstallUninstall(true)}} color="success">Install</Button>
          </Grid>
          <Grid item margin={2}>
            <Button variant="outlined" onClick={() => {handleInstallUninstall(false)}} color="error">Uninstall</Button>
          </Grid>
          <Grid item margin={2}>
            <Button variant="outlined" onClick={() => {handlePing()}} color="warning">Ping</Button>
          </Grid>
        </Grid>
      </Grid>
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={backdropOpen}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={6000}
        onClose={() => {setSnackbarOpen(false);}}
      >
        <Alert 
          onClose={() => {setSnackbarOpen(false);}} 
          severity={messageColor}
          sx={{ width: "100%" }}
          action={snackbaraction}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
      <Dialog
        open={dialogOpen}
        onClose={() => {setDialogOpen(false);}}
        scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title">Ping Results</DialogTitle>
        <DialogContent dividers={true}>
          <DialogContentText
            id="scroll-dialog-description"
            ref={descriptionElementRef}
            tabIndex={-1}
          >
            {dialogMessage.split("\n").map((i, key) => {
              // preserve the number of spaces at the beginning of the line
              let spaces = 0;
              while (i[spaces] === " ") {
                spaces++;
              }
              return (
                <span key={key} style={{ marginLeft: spaces * 10 }}>
                  {i}<br />
                </span>
              );
            })}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {setDialogOpen(false);}} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
