import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import TreeView from '@mui/lab/TreeView';
import TreeItem from '@mui/lab/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import CircularProgress from '@mui/material/CircularProgress';
import { Backdrop } from '@mui/material';

export default function Tree() {
	const dispatch = useDispatch();
	const [fileList, setFileList] = useState(
		useSelector((state) => state.fileList.fileList)
	);
	const [selectedFile, setSelectedFile] = useState(
		useSelector((state) => state.selectedFile.selectedFile)
	);
	useEffect(() => {
		fetch(`${process.env.REACT_APP_API_URL}/editor/files`)
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
				dispatch({ type: 'fileList/setFileList', payload: data });
			});
	}, []);

	const fetchFile = async (node) => {
		setSelectedFile(node);
		dispatch({ type: 'selectedFile/setSelectedFile', payload: node });
		const response = await fetch(
			`${
				process.env.REACT_APP_API_URL
			}/editor/file/read?path=${encodeURIComponent(node.path)}`,
			{
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
			}
		);
		const data = await response.json();
		dispatch({ type: 'fileContent/setFileContent', payload: data.content });
	};

	const renderTree = (nodes) => (
		<TreeItem
			key={nodes.path}
			nodeId={nodes.path}
			label={nodes.name}
			onClick={() => (nodes.is_file === true ? fetchFile(nodes) : null)}
		>
			{nodes.is_file === true
				? null
				: nodes.items.map((node) => renderTree(node))}
		</TreeItem>
	);

	useEffect(() => {
		// filter everything after /ansible/ to file_path
		let filePath = selectedFile.path;
		if (filePath === undefined) {
			return;
		}
		filePath = filePath.substring(filePath.lastIndexOf('/ansible/') + 9);
		dispatch({ type: 'currentPage/setCurrentPage', payload: filePath });
	}, [selectedFile]);

	if (fileList.length === 0) {
		return (
			<Backdrop
				sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
				open
			>
				<CircularProgress color="inherit" />
			</Backdrop>
		);
	}

	return (
		<div>
			<TreeView
				aria-label="file system navigator"
				defaultCollapseIcon={<ExpandMoreIcon />}
				defaultExpandIcon={<ChevronRightIcon />}
				sx={{ overflow: 'auto', height: '90vh' }}
			>
				{fileList.map((node) => renderTree(node))}
			</TreeView>
		</div>
	);
}
