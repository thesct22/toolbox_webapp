import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Grid from "@mui/material/Grid";
import TreeView from "@mui/lab/TreeView";
import TreeItem from "@mui/lab/TreeItem";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import CircularProgress from "@mui/material/CircularProgress";
import { Backdrop } from "@mui/material";

export default function CodeEditor() {
	const dispatch = useDispatch();
	const [fileList, setFileList] = useState(useSelector((state) => state.fileList.fileList));
	const [selectedFile, setSelectedFile] = useState(useSelector((state) => state.selectedFile.selectedFile));
	const [fileContent, setFileContent] = useState(useSelector((state) => state.fileContent.fileContent));

	useEffect(() => {
		fetch(process.env.REACT_APP_API_URL + "/editor/files")
		.then((response) => response.json())
		.then((data) => {
			// Sort the data so that files are listed after directories and then by name
			data.sort((a, b) => {
				if (a.is_file === b.is_file) {
					return a.name.localeCompare(b.name);
				}
				return a.is_file ? 1 : -1;
			});
			setFileList(data);
			dispatch({ type: "fileList/setFileList", payload: data });
		});
	}, []);

	const renderTree = (nodes) => (
		<TreeItem
			key={nodes.path}
			nodeId={nodes.path}
			label={nodes.name}
			onClick={() =>
				nodes.is_file===true ? fetchFile(nodes) : null
			}
		>
			{nodes.is_file===true ? null : nodes.items.map((node) => renderTree(node))}
		</TreeItem>
	);

	const fetchFile = async (node) => {
		setSelectedFile(node);
		dispatch({ type: "selectedFile/setSelectedFile", payload: node });
		const response = await fetch(process.env.REACT_APP_API_URL + "/editor/file/read?path=" + encodeURIComponent(node.path), {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			},
		});
		const data = await response.json();
		setFileContent(data["content"]);
		dispatch({ type: "fileContent/setFileContent", payload: data["content"] });
	};

	useEffect(() => {
		dispatch({ type: "currentPage/setCurrentPage", payload: "Code Editor" });
	}, [dispatch]);

	if (fileList.length === 0) {
		return (
			<Backdrop
				sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
				open={true}
			>
				<CircularProgress color="inherit" />
			</Backdrop>
		);
	}

	return (
		<div>
			<Grid container>
				<Grid item xs={12} md={3}>
					<TreeView
						aria-label="file system navigator"
						defaultCollapseIcon={<ExpandMoreIcon />}
						defaultExpandIcon={<ChevronRightIcon />}
					>
						{fileList.map((node) => renderTree(node))}
					</TreeView>
				</Grid>
				<Grid item xs={12} md={9}>
					<h1>Code Editor</h1>
					<p>CodeEditor page content</p>
					<p>Selected file: {selectedFile.path}</p>
					<p>File content: {fileContent}</p>
				</Grid>
			</Grid>
		</div>
	);
}
