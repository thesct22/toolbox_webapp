import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import TreeView from '@mui/lab/TreeView';
import TreeItem from '@mui/lab/TreeItem';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import CircularProgress from '@mui/material/CircularProgress';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Backdrop from '@mui/material/Backdrop';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

export default function Tree() {
	const dispatch = useDispatch();
	const [fileList, setFileList] = useState(
		useSelector((state) => state.fileList.fileList)
	);
	const [selectedFile, setSelectedFile] = useState(
		useSelector((state) => state.selectedFile.selectedFile)
	);
	const [rightClickedFile, setRightClickedFile] = useState(null);
	const [menuAnchor, setMenuAnchor] = useState(null);
	const [snackBarOpen, setSnackBarOpen] = useState(false);
	const [snackBarMessage, setSnackBarMessage] = useState('');
	const [snackBarSeverity, setSnackBarSeverity] = useState('success');

	const fetchFiles = () => {
		fetch(`${process.env.REACT_APP_API_URL}/editor/files`)
			.then((response) => [response.json(), response.ok])
			.then(async (dataParam) => {
				const data = await dataParam[0];
				const status = dataParam[1];
				if (!status) {
					setSnackBarOpen(true);
					setSnackBarMessage(data.detail);
					setSnackBarSeverity('error');
					return;
				}
				// Sort the data so that files are listed after directories and then by name
				data[0].items.sort((a, b) => {
					if (a.is_file === b.is_file) {
						return a.name.localeCompare(b.name);
					}
					return a.is_file ? 1 : -1;
				});
				setFileList(data);
				dispatch({ type: 'fileList/setFileList', payload: data });
			});
	};
	useEffect(() => {
		fetchFiles();
	}, []);

	const fetchFile = async (node) => {
		setSelectedFile(node);
		dispatch({ type: 'selectedFile/setSelectedFile', payload: node });
		if (node.is_file === true) {
			if (node.name.split('.').length === 1) {
				dispatch({ type: 'language/setLanguage', payload: 'ini' });
			} else {
				const extension = node.name.split('.').pop();
				switch (extension) {
					case 'yml':
						dispatch({ type: 'language/setLanguage', payload: 'yaml' });
						break;
					case 'yaml':
						dispatch({ type: 'language/setLanguage', payload: 'yaml' });
						break;
					case 'json':
						dispatch({ type: 'language/setLanguage', payload: 'json' });
						break;
					case 'ini':
						dispatch({ type: 'language/setLanguage', payload: 'ini' });
						break;
					case 'sh':
						dispatch({ type: 'language/setLanguage', payload: 'shell' });
						break;
					case 'ps1':
						dispatch({ type: 'language/setLanguage', payload: 'powershell' });
						break;
					case 'bat':
						dispatch({ type: 'language/setLanguage', payload: 'bat' });
						break;
					case 'py':
						dispatch({ type: 'language/setLanguage', payload: 'python' });
						break;
					case 'md':
						dispatch({ type: 'language/setLanguage', payload: 'markdown' });
						break;
					default:
						dispatch({ type: 'language/setLanguage', payload: 'plaintext' });
						break;
				}
			}
		}

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
		if (!response.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.detail);
			setSnackBarSeverity('error');
			return;
		}
		dispatch({ type: 'fileContent/setFileContent', payload: data.content });
	};

	const handleRightClick = (event, node) => {
		event.preventDefault();
		event.stopPropagation();
		setRightClickedFile(node);
		setMenuAnchor(event.currentTarget);
	};

	const renderTree = (nodes) => (
		<TreeItem
			id={nodes.path}
			key={nodes.path}
			nodeId={nodes.path}
			label={nodes.name}
			onClick={() => (nodes.is_file === true ? fetchFile(nodes) : null)}
			onContextMenu={(event) => handleRightClick(event, nodes)}
			endIcon={nodes.is_file === true ? null : <ChevronRightIcon />}
		>
			{nodes.is_file === true
				? null
				: nodes.items.map((node) => renderTree(node))}
		</TreeItem>
	);

	const handleNewFile = async (node) => {
		const newName = prompt('Enter new name'); // eslint-disable-line no-alert
		if (newName === null) {
			return;
		}
		const response = await fetch(
			`${process.env.REACT_APP_API_URL}/editor/file/create`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					path: `${node.path}/${newName}`,
				}),
			}
		);
		const data = await response.json();
		if (!response.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.detail);
			setSnackBarSeverity('error');
			return;
		}
		setSnackBarOpen(true);
		setSnackBarMessage('File created successfully');
		setSnackBarSeverity('success');
		fetchFiles();
	};

	const handleNewFolder = async (node) => {
		const newName = prompt('Enter new name'); // eslint-disable-line no-alert
		if (newName === null) {
			return;
		}
		const response = await fetch(
			`${process.env.REACT_APP_API_URL}/editor/folder/create`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					path: `${node.path}/${newName}`,
				}),
			}
		);
		const data = await response.json();
		if (!response.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.detail);
			setSnackBarSeverity('error');
			return;
		}
		setSnackBarOpen(true);
		setSnackBarMessage('Folder created successfully');
		setSnackBarSeverity('success');
		fetchFiles();
	};

	const handleRename = async (node) => {
		const newName = prompt('Enter new name'); // eslint-disable-line no-alert
		if (newName === null) {
			return;
		}
		const repsonse = await fetch(
			`${process.env.REACT_APP_API_URL}/editor/${
				node.is_file ? 'file' : 'folder'
			}/rename`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					path: node.path,
					new_path: newName,
				}),
			}
		);
		const data = await repsonse.json();
		if (!repsonse.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.detail);
			setSnackBarSeverity('error');
			return;
		}
		setSnackBarOpen(true);
		setSnackBarMessage('Renamed successfully');
		setSnackBarSeverity('success');
		fetchFiles();
	};

	const handleDelete = async (node) => {
		// eslint-disable-next-line no-alert
		const confirmDelete = window.confirm(
			`Are you sure you want to delete ${node.name}?`
		);
		if (!confirmDelete) {
			return;
		}
		const response = await fetch(
			`${process.env.REACT_APP_API_URL}/editor/${
				node.is_file ? 'file' : 'folder'
			}/delete`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					path: node.path,
				}),
			}
		);
		const data = await response.json();
		if (!response.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.deatil);
			setSnackBarSeverity('error');
			return;
		}
		if (data.deleted === 'get_confirmation') {
			// eslint-disable-next-line no-alert
			const confirmDeleteForced = window.confirm(
				`Are you really sure you want to delete ${node.name} as it is not empty?` +
					`\nThis will delete all files and folders inside it.`
			);
			if (!confirmDeleteForced) {
				return;
			}
			const confirmResponse = await fetch(
				`${process.env.REACT_APP_API_URL}/editor/${
					node.is_file ? 'file' : 'folder'
				}/delete/confirmed`,
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						path: node.path,
					}),
				}
			);
			const confirmData = await confirmResponse.json();
			if (!confirmResponse.ok) {
				setSnackBarOpen(true);
				setSnackBarMessage(confirmData.detail);
				setSnackBarSeverity('error');
				return;
			}
		}
		setSnackBarOpen(true);
		setSnackBarMessage('Deleted successfully');
		setSnackBarSeverity('success');
		fetchFiles();
	};

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
				defaultExpanded={[fileList[0].path]}
			>
				{fileList.map((node) => renderTree(node))}
			</TreeView>
			<Menu
				id="file-menu"
				anchorEl={menuAnchor}
				open={Boolean(menuAnchor)}
				onClose={() => setMenuAnchor(null)}
			>
				{rightClickedFile && rightClickedFile.is_file ? (
					''
				) : (
					<MenuItem
						onClick={() => {
							handleNewFile(rightClickedFile);
							setMenuAnchor(null);
						}}
					>
						New File
					</MenuItem>
				)}
				{rightClickedFile && rightClickedFile.is_file ? (
					''
				) : (
					<MenuItem
						onClick={() => {
							handleNewFolder(rightClickedFile);
							setMenuAnchor(null);
						}}
					>
						New Folder
					</MenuItem>
				)}
				<MenuItem
					onClick={() => {
						handleRename(rightClickedFile);
						setMenuAnchor(null);
					}}
				>
					Rename
				</MenuItem>
				<MenuItem
					onClick={() => {
						handleDelete(rightClickedFile);
						setMenuAnchor(null);
					}}
				>
					Delete
				</MenuItem>
			</Menu>
			<Snackbar
				open={snackBarOpen}
				autoHideDuration={6000}
				onClose={() => setSnackBarOpen(false)}
			>
				<Alert
					onClose={() => setSnackBarOpen(false)}
					severity={snackBarSeverity}
					sx={{ width: '100%' }}
				>
					{snackBarMessage}
				</Alert>
			</Snackbar>
		</div>
	);
}
