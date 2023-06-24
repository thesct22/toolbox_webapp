import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';


export default function Home() {
  const handleChange = (value) => {
      dispatch({ type: "selectedTags/setSelectedTags", payload: value });
  };
  const dispatch = useDispatch();
  const fetchTags = async () => {
      const response = await fetch(process.env.REACT_APP_API_URL + "/install/tags");
      const data = await response.json();
      dispatch({ type: "tags/setTags", payload: data });
  };

  useEffect(() => {
      fetchTags();
  }, []);

  useEffect(() => {
      dispatch({ type: "currentPage/setCurrentPage", payload: "Installer" });
  }, []);

  return (
    <div>
      <h1>Home</h1>
      <p>Home page content</p>
      <Grid container spacing={4} padding={4}>
        <Grid item xs={12} md={6}>
          <TextField id="username" required label="Username" variant="filled" fullWidth />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField id="password" required label="Password" type="password" variant="filled" fullWidth/>
        </Grid>
        <Grid item xs={12}>
          <TextField id="hosts" required label="Hosts" variant="filled" fullWidth placeholder="IP addresses or hostnames separated by commas"/>
        </Grid>
        <Grid item xs={12}>
          <Autocomplete
              multiple
              id="tags-outlined"
              options={useSelector((state) => state.tags.tags)}
              getOptionLabel={(option) => option.title}
              filterSelectedOptions
              renderInput={(params) => (
              <TextField
                  {...params}
                  label="Select Software"
                  placeholder="Select Software"
              />
              )}
              onChange={(event, value) => {handleChange(value);}}
          />
        </Grid>
      </Grid>
    </div>
  );
}

