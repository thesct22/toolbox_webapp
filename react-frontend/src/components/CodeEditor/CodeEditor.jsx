import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { Alert, Button, Grid, Select, Snackbar, Paper, Typography } from '@mui/material';
import Tree from './Tree';
import EditorWindow from './EditorWindow';

export default function CodeEditor() {
	const dispatch = useDispatch();
	const [snackBarOpen, setSnackBarOpen] = useState(false);
	const [snackBarMessage, setSnackBarMessage] = useState('');
	const selectedFile = useSelector((state) => state.selectedFile.selectedFile);
	const fileContent = useSelector((state) => state.fileContent.fileContent);

	useEffect(() => {
		dispatch({ type: 'currentPage/setCurrentPage', payload: 'Code Editor' });
	}, []);

	const onSave = async () => {
		const response = await fetch(
			`${process.env.REACT_APP_API_URL}/editor/file/write`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					path: selectedFile.path,
					content: fileContent,
				}),
			}
		);
		const data = await response.json();
		if (data.success) {
			setSnackBarMessage('File saved successfully!');
			setSnackBarOpen(true);
		}
		if (!data.success) {
			setSnackBarMessage('File save failed!');
			setSnackBarOpen(true);
		}
	};

	const onReset = async () => {
		const response = await fetch(
			`${
				process.env.REACT_APP_API_URL
			}/editor/file/read?path=${encodeURIComponent(selectedFile.path)}`,
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

	return (
		<div>
			<Grid container>
				<Grid item xs={12} md={3}>
					<Tree />
				</Grid>
				<Grid container item xs={12} md={9}>
					<Grid item xs={12}>
						<Paper elevation={16}>
							<EditorWindow />
						</Paper>
					</Grid>
					<Grid
						container
						item
						spacing={2}
						padding={2}
						direction="row"
						justifyContent="flex-end"
						alignItems="baseline"
					>
						<Grid item xs={4} m={1}>
							<Typography variant="subtitle1" component="div">
								{selectedFile.path!==undefined?selectedFile.path.substring(selectedFile.path.lastIndexOf('/ansible/') + 9):''}
							</Typography>
						</Grid>
						<Grid item>
							<Select
								native
								value={useSelector((state) => state.language.language)}
								onChange={(event) => {
									dispatch({
										type: 'language/setLanguage',
										payload: event.target.value,
									});
								}}
								size="small"
							>
								<option value="yaml">YAML</option>
								<option value="json">JSON</option>
								<option value="ini">INI</option>
								<option value="shell">Shell</option>
								<option value="powershell">PowerShell</option>
								<option value="bat">Batch</option>
								<option value="python">Python</option>
								<option value="markdown">Markdown</option>
								<option value="plaintext">Plain Text</option>
							</Select>
						</Grid>

						<Grid item>
							<Button
								variant="contained"
								color="success"
								onClick={() => onSave()}
							>
								Save
							</Button>
						</Grid>
						<Grid item>
							<Button
								variant="contained"
								color="error"
								onClick={() => onReset()}
							>
								Reset
							</Button>
						</Grid>
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
					severity={
						snackBarMessage === 'File saved successfully!' ? 'success' : 'error'
					}
				>
					{snackBarMessage}
				</Alert>
			</Snackbar>
		</div>
	);
}
