import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as forge from 'node-forge';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';

export default function ConfigureTarget() {
	const dispatch = useDispatch();
	const [rsaKey, setRsaKey] = React.useState('');
	const [username, setUsername] = React.useState('');
	const [password, setPassword] = React.useState('');
	const [hosts, setHosts] = React.useState(
		useSelector((state) => state.hosts.hosts)
	);
	const [snackbarOpen, setSnackbarOpen] = React.useState(false);
	const [snackbarMessage, setSnackbarMessage] = React.useState('');
	const [messageColor, setMessageColor] = React.useState('success');

	const fetchRSAKey = async () => {
		const response = await fetch(`${process.env.REACT_APP_API_URL}/public_key`);
		const data = await response.json();
		setRsaKey(data.public_key);
	};

	React.useEffect(() => {
		fetchRSAKey();
	}, []);

	const usernameChanged = (event) => {
		setUsername(event.target.value);
	};
	const passwordChanged = (event) => {
		setPassword(event.target.value);
	};

	const hostsChanged = (event) => {
		setHosts(event.target.value);
		dispatch({ type: 'hosts/setHosts', payload: event.target.value });
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

	const publicKey = forge.pki.publicKeyFromPem(rsaKey);
	const encrypt = (text) => {
		const encrypted = publicKey.encrypt(text, 'RSA-OAEP', {
			md: forge.md.sha256.create(),
			mgf1: {
				md: forge.md.sha256.create(),
			},
		});
		return forge.util.encode64(encrypted);
	};

	const handleClick = () => {
		const encryptedUsername = encrypt(username);
		const encryptedPassword = encrypt(password);
		const encryptedHosts = encrypt(hosts);

		fetch(`${process.env.REACT_APP_API_URL}/target/configure`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				user: encryptedUsername,
				password: encryptedPassword,
				hosts: encryptedHosts,
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
				setMessageColor('success');
				setSnackbarMessage('Target(s) configured successfully');
			})
			.catch((error) => {
				setSnackbarOpen(true);
				setMessageColor('error');
				setSnackbarMessage(`Error: ${error.message}`);
			});
	};

	const snackbaraction = (
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
	);

	return (
		<div>
			<h1>Configure Target</h1>
			<p>ConfigureTarget page content</p>
			<Grid container spacing={3}>
				<Grid item xs={12} md={6}>
					<TextField
						id="username"
						required
						label="Username"
						variant="filled"
						fullWidth
						onChange={usernameChanged}
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
						onChange={passwordChanged}
						value={password}
					/>
				</Grid>
				<Grid item xs={12}>
					<TextField
						id="hosts"
						required
						label="Hosts"
						variant="filled"
						fullWidth
						placeholder="IP addresses or hostnames separated by commas"
						onChange={hostsChanged}
						value={hosts}
					/>
				</Grid>
				<Grid item xs={12}>
					<Button onClick={handleClick}>Configure</Button>
				</Grid>
			</Grid>
			<Snackbar
				open={snackbarOpen}
				autoHideDuration={6000}
				onClose={() => setSnackbarOpen(false)}
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
		</div>
	);
}
