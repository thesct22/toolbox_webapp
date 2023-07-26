import React, { useEffect, useState } from 'react';
import forge from 'node-forge';
import {
	Alert,
	Backdrop,
	Button,
	CircularProgress,
	Dialog,
	DialogActions,
	DialogContent,
	DialogContentText,
	DialogTitle,
	IconButton,
	Snackbar,
	Grid,
	TextField,
	Typography,
	Slider,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

// eslint-disable-next-line
export default function CustomForm({ playbookPath, inventoryPath }) {
	const [rsaKey, setRsaKey] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [verbosity, setVerbosity] = useState(0);
	const [tags, setTags] = useState('');
	const [extraArgs, setExtraArgs] = useState('');
	const [extraVars, setExtraVars] = useState([{ key: '', value: '' }]);
	const [backdropOpen, setBackdropOpen] = useState(false);
	const [snackbarOpen, setSnackbarOpen] = useState(false);
	const [snackbarMessage, setSnackbarMessage] = useState('');
	const [messageColor, setMessageColor] = useState('success');
	const [dialogMessage, setDialogMessage] = useState('');
	const [dialogOpen, setDialogOpen] = useState(false);

	const fetchRSAKey = async () => {
		const response = await fetch(`${process.env.REACT_APP_API_URL}/public_key`);
		const data = await response.json();
		setRsaKey(data.public_key);
	};

	const descriptionElementRef = React.useRef(null);
	useEffect(() => {
		if (dialogOpen) {
			const { current: descriptionElement } = descriptionElementRef;
			if (descriptionElement !== null) {
				descriptionElement.focus();
			}
		}
	}, [dialogOpen]);

	useEffect(() => {
		fetchRSAKey();
	}, []);
	let publicKey = '';
	if (rsaKey !== '') {
		publicKey = forge.pki.publicKeyFromPem(rsaKey);
	} else {
		publicKey = '';
	}
	const encrypt = (text) => {
		const encrypted = publicKey.encrypt(text, 'RSA-OAEP', {
			md: forge.md.sha256.create(),
			mgf1: {
				md: forge.md.sha256.create(),
			},
		});
		return forge.util.encode64(encrypted);
	};

	if (rsaKey === '') {
		return (
			<Backdrop
				sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
				open
			>
				<CircularProgress color="inherit" />
			</Backdrop>
		);
	}

	const handlePing = () => {
		setBackdropOpen(true);
		const encryptedUsername = encrypt(username);
		const encryptedPassword = encrypt(password);
		const encryptedHosts = encrypt(inventoryPath);

		fetch(`${process.env.REACT_APP_API_URL}/target/ping`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				hosts: encryptedHosts,
				user: encryptedUsername,
				password: encryptedPassword,
				verbosity,
			}),
		})
			.then((response) => [response.json(), response.ok])
			.then(async (dataParam) => {
				const status = dataParam[1];
				const data = await dataParam[0];
				if (!status) {
					throw new Error(data.detail);
				}
				setSnackbarOpen(true);
				setSnackbarMessage('Ping successful');
				setBackdropOpen(false);
				setMessageColor('success');
				setDialogMessage(data);
			})
			.catch((error) => {
				setSnackbarOpen(true);
				setSnackbarMessage('Ping failed');
				setBackdropOpen(false);
				setMessageColor('error');
				setDialogMessage(error.message);
			});
	};

	const handleRun = () => {
		setBackdropOpen(true);
		const encryptedUsername = encrypt(username);
		const encryptedPassword = encrypt(password);
		const encryptedPlaybook = encrypt(playbookPath);
		const encryptedInventory = encrypt(inventoryPath);
		const encryptedTags = encrypt(tags);
		const encryptedExtraArgs = encrypt(extraArgs);
		// select all extraVars where key and value are not empty
		const encryptedExtraVars = encrypt(
			JSON.stringify(
				extraVars.filter(
					(extraVar) => extraVar.key !== '' && extraVar.value !== ''
				)
			)
		);

		fetch(`${process.env.REACT_APP_API_URL}/custom/run`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				playbook: encryptedPlaybook,
				hosts: encryptedInventory,
				user: encryptedUsername,
				password: encryptedPassword,
				verbosity,
				tags: encryptedTags,
				extra_args: encryptedExtraArgs,
				extra_vars: encryptedExtraVars,
			}),
		})
			.then((response) => [response.json(), response.ok])
			.then(async (dataParam) => {
				const status = dataParam[1];
				const data = await dataParam[0];
				if (!status) {
					throw new Error(data.detail);
				}
				setSnackbarOpen(true);
				setSnackbarMessage('Playbook run successful');
				setBackdropOpen(false);
				setMessageColor('success');
				setDialogMessage(data);
			})
			.catch((error) => {
				setSnackbarOpen(true);
				setSnackbarMessage('Playbook run failed');
				setBackdropOpen(false);
				setMessageColor('error');
				setDialogMessage(error.message);
			});
	};

	const onVerbosityChange = (value) => {
		setVerbosity(value);
	};

	const onTagChange = (value) => {
		setTags(value);
	};

	const snackbaraction = (
		<>
			<Button
				color="secondary"
				size="small"
				onClick={() => {
					setDialogOpen(true);
				}}
			>
				View Details
			</Button>
			<IconButton
				size="small"
				aria-label="close"
				color="inherit"
				onClick={() => {
					setSnackbarOpen(false);
				}}
			>
				<CloseIcon fontSize="small" />
			</IconButton>
		</>
	);

	return (
		<div>
			<Grid container spacing={1} marginTop={2} paddingRight={2}>
				<Grid item xs={12} md={6}>
					<TextField
						id="username"
						required
						label="Username"
						variant="filled"
						fullWidth
						onChange={(event) => {
							setUsername(event.target.value);
						}}
						value={username}
						size="small"
					/>
				</Grid>
				<Grid item xs={12} md={6}>
					<TextField
						id="password"
						required
						label="Password"
						type="password"
						variant="filled"
						fullWidth
						onChange={(event) => {
							setPassword(event.target.value);
						}}
						value={password}
						size="small"
					/>
				</Grid>
				<Grid item xs={12} alignItems="center">
					<Typography variant="h6" gutterBottom align="left">
						Playbook:{' '}
						{playbookPath
							? playbookPath.split('ansible/')[1] // eslint-disable-line
							: 'No playbook selected'}{' '}
					</Typography>
				</Grid>
				<Grid item xs={12} alignItems="center">
					<Typography variant="h6" gutterBottom align="left">
						Inventory:{' '}
						{inventoryPath
							? inventoryPath.split('ansible/')[1] // eslint-disable-line
							: 'No inventory selected'}{' '}
					</Typography>
				</Grid>
				<Grid item container xs>
					<Grid item container xs={12} md={6} alignItems="center">
						<Grid item sx={{ alignItems: 'center' }}>
							<Typography variant="h6" gutterBottom>
								Verbosity:
							</Typography>
						</Grid>
						<Grid item xs padding={2}>
							<Slider
								aria-label="Verbosity"
								valueLabelDisplay="auto"
								step={1}
								marks
								min={0}
								max={4}
								value={verbosity}
								onChange={(_, value) => {
									onVerbosityChange(value);
								}}
							/>
						</Grid>
					</Grid>
					<Grid item xs={12} md={6}>
						<TextField
							id="tags"
							label="Tags"
							variant="filled"
							fullWidth
							onChange={(event) => {
								onTagChange(event.target.value);
							}}
							value={tags}
							size="small"
						/>
					</Grid>
				</Grid>
				<Grid item xs={12}>
					<TextField
						id="extra_args"
						label="Extra Arguments"
						variant="filled"
						fullWidth
						value={extraArgs}
						onChange={(event) => {
							setExtraArgs(event.target.value);
						}}
						size="small"
					/>
				</Grid>
				<Grid item xs={12} alignItems="center">
					<Typography variant="h6" gutterBottom align="left">
						Extra Variables:
					</Typography>
				</Grid>
				<Grid item xs={12}>
					{extraVars.map((extraVar, index) => (
						<Grid
							container
							spacing={1}
							key={`extra-var-${index}`} // eslint-disable-line
							alignItems="center"
						>
							<Grid item xs={5}>
								<TextField
									id={`extra-var-key-${index}`}
									label="Key"
									variant="filled"
									fullWidth
									value={extraVar.key}
									onChange={(event) => {
										const newExtraVars = [...extraVars];
										newExtraVars[index].key = event.target.value;
										setExtraVars(newExtraVars);
										if (
											index === extraVars.length - 1 &&
											event.target.value !== ''
										) {
											setExtraVars([...extraVars, { key: '', value: '' }]);
										}
										if (
											index === extraVars.length - 2 &&
											event.target.value === '' &&
											extraVars.length > 1 &&
											extraVars[index].value === ''
										) {
											setExtraVars(extraVars.slice(0, -1));
										}
									}}
									size="small"
								/>
							</Grid>
							<Typography variant="h4" gutterBottom align="center">
								{' :'}
							</Typography>
							<Grid item xs={5}>
								<TextField
									id={`extra-var-value-${index}`}
									label="Value"
									variant="filled"
									fullWidth
									value={extraVar.value}
									onChange={(event) => {
										const newExtraVars = [...extraVars];
										newExtraVars[index].value = event.target.value;
										setExtraVars(newExtraVars);
										if (
											index === extraVars.length - 1 &&
											event.target.value !== ''
										) {
											setExtraVars([...extraVars, { key: '', value: '' }]);
										}
										if (
											index === extraVars.length - 2 &&
											event.target.value === '' &&
											extraVars.length > 1 &&
											extraVars[index].key === ''
										) {
											setExtraVars(extraVars.slice(0, -1));
										}
									}}
									size="small"
								/>
							</Grid>
						</Grid>
					))}
				</Grid>
				<Grid item container>
					<Grid item margin={2} marginLeft={0}>
						<Button
							variant="contained"
							onClick={() => {
								handleRun();
							}}
							color="success"
						>
							Run
						</Button>
					</Grid>
					<Grid item margin={2}>
						<Button
							variant="contained"
							onClick={() => {
								handlePing();
							}}
							color="warning"
						>
							Ping
						</Button>
					</Grid>
				</Grid>
			</Grid>
			<Backdrop
				sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
				open={backdropOpen}
			>
				<CircularProgress color="inherit" />
			</Backdrop>
			<Snackbar
				open={snackbarOpen}
				autoHideDuration={6000}
				onClose={() => {
					setSnackbarOpen(false);
				}}
			>
				<Alert
					onClose={() => {
						setSnackbarOpen(false);
					}}
					severity={messageColor}
					sx={{ width: '100%' }}
					action={snackbaraction}
				>
					{snackbarMessage}
				</Alert>
			</Snackbar>
			<Dialog
				open={dialogOpen}
				onClose={() => {
					setDialogOpen(false);
				}}
				scroll="paper"
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
			>
				<DialogTitle id="scroll-dialog-title">Ping Results</DialogTitle>
				<DialogContent dividers>
					<DialogContentText
						id="scroll-dialog-description"
						ref={descriptionElementRef}
						tabIndex={-1}
					>
						{dialogMessage.split('\n').map((message, messageIndex) => {
							// preserve the number of spaces at the beginning of the line
							let spaces = 0;
							while (message[spaces] === ' ') {
								spaces += 1;
							}
							const key = `dialog-message-${message}-${messageIndex}`;
							return (
								<span key={key} style={{ marginLeft: spaces * 10 }}>
									{message}
									<br />
								</span>
							);
						})}
					</DialogContentText>
				</DialogContent>
				<DialogActions>
					<Button
						onClick={() => {
							setDialogOpen(false);
						}}
						color="primary"
					>
						Close
					</Button>
				</DialogActions>
			</Dialog>
		</div>
	);
}
