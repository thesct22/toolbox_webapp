import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

export default function Terminal() {

    const dispatch = useDispatch();

    useEffect(() => {
        dispatch({ type: "currentPage/setCurrentPage", payload: "Terminal" });
    }, []);
    return (
        <div>
        <h1>Terminal</h1>
        <p>Terminal page content</p>
        </div>
    );
    }
