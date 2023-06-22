import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";

export default function Home() {

    const [tags, setTags] = useState({});
    // const [selectedTags, setSelectedTags] = useState({});
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
        </div>
    );}

