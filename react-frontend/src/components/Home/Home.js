import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';


export default function Home() {
    const handleChange = (value) => {
        dispatch({ type: "selectedTags/setSelectedTags", payload: value });
    };
    const dispatch = useDispatch();
    const fetchTags = async () => {
        const response = await fetch("http://localhost:8000/api/install/tags");
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
        </div>
    );}

