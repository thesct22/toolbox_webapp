import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
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
	// Slider,
	TextField,
	Typography,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

export default function CustomForm({ playbookPath, inventoryPath }) {
	// eslint-disable-line
	const [rsaKey, setRsaKey] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
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
		const encryptedHosts = encrypt(
			useSelector((state) => state.inventory.inventory)
		);

		fetch(`${process.env.REACT_APP_API_URL}/target/ping`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				hosts: encryptedHosts,
				user: encryptedUsername,
				password: encryptedPassword,
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
		const encryptedPlaybook = encrypt(
			useSelector((state) => state.playbook.playbook)
		);
		const encryptedInventory = encrypt(
			useSelector((state) => state.inventory.inventory)
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
					/>
				</Grid>
				<Grid item xs={12}>
					<Typography variant="h6" gutterBottom component="div" align="left">
						Playbook:{' '}
						{playbookPath
							? playbookPath.split('ansible/')[1]
							: 'No playbook selected'}{' '}
						{/*eslint-disable-line*/}
					</Typography>
				</Grid>
				<Grid item xs={12}>
					<Typography variant="h6" gutterBottom component="div" align="left">
						Inventory:{' '}
						{inventoryPath
							? inventoryPath.split('ansible/')[1]
							: 'No inventory selected'}{' '}
						{/*eslint-disable-line*/}
					</Typography>
				</Grid>
				<Grid item container>
					<Grid item margin={2} marginLeft={0}>
						<Button
							variant="outlined"
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
							variant="outlined"
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
