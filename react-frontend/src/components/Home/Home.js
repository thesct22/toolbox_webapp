import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Select from "@mui/material/Select";
import { useTheme } from '@mui/material/styles';
import { MenuItem } from "@mui/material";
import OutlinedInput from '@mui/material/OutlinedInput';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
    PaperProps: {
        style: {
            maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
            width: 250,
        },
    },
};

function getStyles(name, selectedTags, theme) {
    return {
        fontWeight:
        selectedTags.indexOf(name) === -1
            ? theme.typography.fontWeightRegular
            : theme.typography.fontWeightMedium,
    };
}

export default function Home() {
    const theme = useTheme();
    const [tags, setTags] = useState({});
    const [selectedTags, setSelectedTags] = useState([]);
    const handleChange = (event) => {
        const {
          target: { value },
        } = event;
        setSelectedTags(
          // On autofill we get a stringified value.
          typeof value === 'string' ? value.split(',') : value,
        );
      };
    // fetch data from the http://localhost:8000/api/install/tags endpoint of backend and add it to the redux store
    const dispatch = useDispatch();
    const fetchTags = async () => {
        const response = await fetch("http://localhost:8000/api/install/tags");
        const data = await response.json();
        dispatch({ type: "tags/setTags", payload: data });
        setTags(data);
        console.log(data);
    };

    useEffect(() => {
        fetchTags();
    }, );

    return (
        <div>
        <h1>Home</h1>
        <p>Home page content</p>
        {/* list the tags which is an dictionary */}
        <List sx={{ width: "100%", maxWidth: 360, bgcolor: "background.black" }}>
            {Object.keys(tags).map((name, index) => (
                <ListItem key={index}>
                    <ListItemText primary={name} secondary={tags[name][0]} />
                    {/* <ul>
                        {tags[name].map((tag) => (
                            <li key={tag}>{tag}</li>
                        ))}
                    </ul> */}
                </ListItem>
            ))}
        </List>
        <Select
          labelId="demo-multiple-name-label"
          id="demo-multiple-name"
          multiple
          value={selectedTags}
          onChange={handleChange}
          input={<OutlinedInput label="Name" />}
          MenuProps={MenuProps}
        >
          {Object.keys(tags).map((name, index) => (
            <MenuItem
              key={name}
              value={name}
              style={getStyles(name, selectedTags, theme)}
            >
              {name}
            </MenuItem>
          ))}
        </Select>
        </div>
    );}

