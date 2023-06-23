import React, { useEffect } from "react";
import { useDispatch } from "react-redux";

export default function CodeEditor() {
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch({ type: "currentPage/setCurrentPage", payload: "Code Editor" });
    }, [dispatch]);

    return (
        <div>
            <h1>Code Editor</h1>
            <p>CodeEditor page content</p>
        </div>
    );
}
