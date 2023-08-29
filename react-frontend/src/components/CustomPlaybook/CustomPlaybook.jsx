import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Backdrop, Grid, Typography, Snackbar, Alert, Paper } from '@mui/material';
import { TreeView, TreeItem } from '@mui/lab';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import CircularProgress from '@mui/material/CircularProgress';
import Editor from '@monaco-editor/react';
import CustomForm from './CustomForm';

export default function CustomPlaybook() {
	const dispatch = useDispatch();
	const [fileContent, setFileContent] = useState(
		useSelector((state) => state.fileContent.fileContent)
	);
	const [language, setLanguage] = useState(
		useSelector((state) => state.language.language)
	);
	const [playbook, setPlaybook] = useState(
		useSelector((state) => state.playbook.playbook)
	);
	const [inventory, setInventory] = useState(
		useSelector((state) => state.inventory.inventory)
	);
	const [playbooks, setPlaybooks] = useState([]);
	const [inventories, setInventories] = useState([]);
	const [snackBarOpen, setSnackBarOpen] = useState(false);
	const [snackBarMessage, setSnackBarMessage] = useState('');
	const [snackBarSeverity, setSnackBarSeverity] = useState('success');

	useEffect(() => {
		fetch(`${process.env.REACT_APP_API_URL}/custom/playbooks`)
			.then((res) => res.json())
			.then((data) => setPlaybooks(data))
			.catch((err) => {
				setSnackBarOpen(true);
				setSnackBarMessage(err);
				setSnackBarSeverity('error');
			});

		fetch(`${process.env.REACT_APP_API_URL}/custom/inventories`)
			.then((res) => res.json())
			.then((data) => setInventories(data))
			.catch((err) => {
				setSnackBarOpen(true);
				setSnackBarMessage(err);
				setSnackBarSeverity('error');
			});
		dispatch({
			type: 'currentPage/setCurrentPage',
			payload: 'Custom Playbook Runner',
		});
	}, []);

	if (playbooks.length === 0 || inventories.length === 0) {
		return (
			<Backdrop
				sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
				open
			>
				<CircularProgress color="inherit" />
			</Backdrop>
		);
	}

	const fetchFile = async (node) => {
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
		if (!response.ok) {
			setSnackBarOpen(true);
			setSnackBarMessage(data.detail);
			setSnackBarSeverity('error');
			return;
		}
		setFileContent(data.content);
		dispatch({ type: 'fileContent/setFileContent', payload: data.content });
	};

	const onPlaybookSelect = (value) => {
		if (value.path === playbook.path) {
			setPlaybook('');
			dispatch({ type: 'playbook/setPlaybook', payload: '' });
			return;
		}
		setLanguage('yaml');
		setPlaybook(value);
		dispatch({ type: 'language/setLanguage', payload: 'yaml' });
		dispatch({ type: 'playbook/setPlaybook', payload: value });
		fetchFile(value);
	};

	const onInventorySelect = (value) => {
		if (value.is_file === false) {
			return;
		}
		if (value.path === inventory.path) {
			setInventory('');
			dispatch({ type: 'inventory/setInventory', payload: '' });
			return;
		}
		setLanguage('ini');
		setInventory(value);
		dispatch({ type: 'language/setLanguage', payload: 'ini' });
		dispatch({ type: 'inventory/setInventory', payload: value });
		fetchFile(value);
	};

	const renderTree = (nodes) => (
		<TreeItem
			id={nodes.path}
			key={nodes.path}
			nodeId={nodes.path}
			label={nodes.name}
			onClick={() => onInventorySelect(nodes)}
			endIcon={nodes.is_file === true ? null : <ChevronRightIcon />}
		>
			{nodes.is_file === true
				? null
				: nodes.items.map((node) => renderTree(node))}
		</TreeItem>
	);

	return (
		<div>
			<Grid container>
				<Grid item xs={12} md={3}>
					<Typography variant="overline">Custom Playbooks</Typography>
					<TreeView
						aria-label="Playbooks"
						defaultCollapseIcon={<ExpandMoreIcon />}
						defaultExpandIcon={<ChevronRightIcon />}
					>
						{playbooks.map((playbookOption) => (
							<TreeItem
								key={playbookOption.path}
								nodeId={playbookOption.path}
								label={playbookOption.name}
								onClick={() => onPlaybookSelect(playbookOption)}
							/>
						))}
					</TreeView>
					<Typography variant="overline">Custom Inventories</Typography>
					<TreeView
						aria-label="Inventory files"
						defaultCollapseIcon={<ExpandMoreIcon />}
						defaultExpandIcon={<ChevronRightIcon />}
					>
						{inventories.map((inventoryOption) => renderTree(inventoryOption))}
					</TreeView>
				</Grid>
				<Grid container item xs={12} md={9}>
					<Grid item xs={12}>
						<Paper elevation={16}>
							<Editor
								height="50vh"
								defaultLanguage="yaml"
								language={language}
								value={fileContent}
								theme={localStorage.getItem('theme') === 'dark' ? 'vs-dark' : 'light'}
								options={{
									readOnly: true,
									minimap: {
										enabled: true,
									},
									automaticLayout: true,
									wrappingIndent: 'indent',
									wordWrap: 'on',
									wordWrapColumn: 80,
									wordWrapMinified: true,
									scrollBeyondLastLine: false,
									scrollbar: {
										alwaysConsumeMouseWheel: false,
									},
								}}
							/>
						</Paper>
					</Grid>
					<Grid item xs={12}>
						<Paper elevation={16} sx={{p:2}}>
							<CustomForm
								playbookPath={playbook.path}
								inventoryPath={inventory.path}
							/>
						</Paper>
					</Grid>
				</Grid>
			</Grid>
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
