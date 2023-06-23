import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

export default function Instructions() {

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch({ type: "currentPage/setCurrentPage", payload: "Instructions" });
    }, []);

    return (
        <div>
        <h1>Instructions for Users</h1>
        <p>Instructions page content</p>
        </div>
    );
    }
