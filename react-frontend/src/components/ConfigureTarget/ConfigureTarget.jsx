import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as forge from 'node-forge';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import { Typography } from '@mui/material';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';

import BackgroundImage from './BackgroundImage.jpg';

export default function ConfigureTarget() {
	const dispatch = useDispatch();
	const [rsaKey, setRsaKey] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [hosts, setHosts] = useState(useSelector((state) => state.hosts.hosts));
	const [snackbarOpen, setSnackbarOpen] = useState(false);
	const [snackbarMessage, setSnackbarMessage] = useState('');
	const [messageColor, setMessageColor] = useState('success');

	const fetchRSAKey = async () => {
		const response = await fetch(`${process.env.REACT_APP_API_URL}/public_key`);
		const data = await response.json();
		setRsaKey(data.public_key);
	};

	useEffect(() => {
		fetchRSAKey();
		dispatch({
			type: 'currentPage/setCurrentPage',
			payload: 'Configure Target',
		});
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
				data-testid="loading-backdrop"
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
		let hostsRaw = hosts.replace(/,|\s|\n/g, ',');
		hostsRaw = hostsRaw.replace(/,{2,}/g, ',').replace(/,$/, '');
		const encryptedHosts = encrypt(hostsRaw);

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
		<div
			// align the paper to the right middle of the screen
			style={{
				display: 'flex',
				justifyContent: 'flex-end',
				alignItems: 'center',
				height: 'calc(100vh - 64px)',
				background: `url(${BackgroundImage}) no-repeat center center fixed`,
				backgroundSize: 'cover',
			}}
		>
			<Paper
				sx={{
					p: 2,
					display: 'flex',
					justifyContent: 'center',
					alignItems: 'center',
					width: 'fit-content',
					height: '100%',
					alignContent: 'center',
					backgroundColor: 'rgba(255, 255, 255, 0.7)',
				}}
				elevation={4}
			>
				<Paper
					sx={{ p: 2, m: 2, height: 'fit-content', width: '100%' }}
					elevation={4}
				>
					<Stack
						direction="column"
						justifyContent="center"
						alignItems="center"
						spacing={2}
						sx={{ width: '100%' }}
					>
						<TextField
							id="username"
							required
							label="Username"
							size="small"
							variant="filled"
							fullWidth
							sx={{ width: '25vw' }}
							onChange={usernameChanged}
							value={username}
						/>
						<TextField
							id="password"
							required
							label="Password"
							type="password"
							size="small"
							variant="filled"
							fullWidth
							sx={{ width: '25vw' }}
							onChange={passwordChanged}
							value={password}
						/>
						<TextField
							id="hosts"
							required
							label="Hostnames/IP Addresses"
							size="small"
							variant="filled"
							multiline
							fullWidth
							sx={{ width: '25vw' }}
							maxRows={4}
							placeholder="Separated by commas, spaces or newlines"
							onChange={hostsChanged}
							value={hosts}
						/>
						<Button onClick={handleClick} variant="contained" color="warning">
							Configure
						</Button>
					</Stack>
				</Paper>
			</Paper>
			<Typography
				variant="caption"
				sx={{
					position: 'absolute',
					bottom: 0,
					right: 0,
					m: 1,
					color: 'white',
				}}
			>
				<a href="https://www.freepik.com/free-vector/technical-support-guys-working-repairing-computer-hardware-software-troubleshooting-fixing-problems-problem-checking-concept-bright-vibrant-violet-isolated-illustration_10780432.htm#query=webapp%20toolbox%20configure%20remote%20machines&position=24&from_view=search&track=ais">
					Image by vectorjuice
				</a>{' '}
				on Freepik
			</Typography>
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
					data-testid="snackbar"
				>
					{snackbarMessage}
				</Alert>
			</Snackbar>
		</div>
	);
}
