import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import * as forge from 'node-forge';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import Button from '@mui/material/Button';
import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import Snackbar from '@mui/material/Snackbar';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useNavigate } from 'react-router-dom';

import BackgroundImage from './BackgroundImage.jpg';

export default function Home() {
	const dispatch = useDispatch();
	const navigate = useNavigate();
	const [rsaKey, setRsaKey] = useState('');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [hosts, setHosts] = useState(useSelector((state) => state.hosts.hosts));
	const [tags, setTags] = useState(useSelector((state) => state.tags.tags));
	const [selectedTags, setSelectedTags] = useState(
		useSelector((state) => state.selectedTags.selectedTags)
	);
	const [backdropOpen, setBackdropOpen] = useState(false);
	const [snackbarOpen, setSnackbarOpen] = useState(false);
	const [snackbarMessage, setSnackbarMessage] = useState('');
	const [messageColor, setMessageColor] = useState('success');
	const [dialogOpen, setDialogOpen] = useState(false);
	const [dialogMessage, setDialogMessage] = useState('');
	const [showNavigateButton, setShowNavigateButton] = useState(false);

	const fetchTags = async () => {
		const installResponse = await fetch(
			`${window.location.origin}/api/install/tags`
		);
		const installData = await installResponse.json();
		const uninstallResponse = await fetch(
			`${window.location.origin}/api/uninstall/tags`
		);
		const uninstallData = await uninstallResponse.json();
		const data = [...installData];
		for (let i = 0; i < uninstallData.length; i += 1) {
			if (!data.some((item) => item.title === uninstallData[i].title)) {
				uninstallData[i].title = `${uninstallData[i].title} (uninstall only)`;
				data.push(uninstallData[i]);
			}
		}
		for (let i = 0; i < installData.length; i += 1) {
			if (!uninstallData.some((item) => item.title === installData[i].title)) {
				const index = data.findIndex(
					(item) => item.title === `${installData[i].title}`
				);
				data.splice(index, 1);
				installData[i].title = `${installData[i].title} (install only)`;
				data.push(installData[i]);
			}
		}
		setTags(data);
		dispatch({ type: 'tags/setTags', payload: data });
	};

	const fetchRSAKey = async () => {
		const response = await fetch(`${window.location.origin}/api/public_key`);
		const data = await response.json();
		setRsaKey(data.public_key);
	};

	useEffect(() => {
		fetchTags();
		fetchRSAKey();
		setMessageColor('warning');
		setShowNavigateButton(true);
		setDialogMessage(
			'Go to the Configure Target page to configure your target machine(s).\nThis needs to be done only once for each target machine.\nIf you are running this webapp using a docker container you will have to configure the target machine(s) again if you are using a new container.\nOnce configured, you can run the installer and uninstaller from this page as many times as you wish without having to reconfigure.'
		);
		setSnackbarMessage(
			"Don't forget to configure your target machine(s) first if you are connecting to them for the first time using this machine."
		);
		setSnackbarOpen(true);
	}, []);

	useEffect(() => {
		dispatch({ type: 'currentPage/setCurrentPage', payload: 'Installer' });
	}, []);

	const descriptionElementRef = React.useRef(null);
	useEffect(() => {
		if (dialogOpen) {
			const { current: descriptionElement } = descriptionElementRef;
			if (descriptionElement !== null) {
				descriptionElement.focus();
			}
		}
	}, [dialogOpen]);

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

	const handleSoftwareListChange = (value) => {
		const tagsList = [];
		value.map((softwareItem) => {
			softwareItem.tags.map((tag) => {
				if (!tagsList.includes(tag)) {
					tagsList.push(tag);
				}
				return null;
			});
			return null;
		});
		setSelectedTags(tagsList);
		dispatch({ type: 'selectedTags/setSelectedTags', payload: tagsList });
	};

	const handleHostsChange = (value) => {
		setHosts(value);
		dispatch({ type: 'hosts/setHosts', payload: value });
	};

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

	const handlePing = () => {
		setBackdropOpen(true);
		const encryptedUsername = encrypt(username);
		const encryptedPassword = encrypt(password);
		let hostsRaw = hosts.replace(/,|\s|\n/g, ',');
		hostsRaw = hostsRaw.replace(/,{2,}/g, ',').replace(/,$/, '');
		const encryptedHosts = encrypt(hostsRaw);

		fetch(`${window.location.origin}/api/target/ping`, {
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
				setShowNavigateButton(false);
				setSnackbarOpen(true);
				setSnackbarMessage('Ping successful');
				setBackdropOpen(false);
				setMessageColor('success');
				setDialogMessage(data);
			})
			.catch((error) => {
				if (error.message.includes('Failed to fetch')) {
					setShowNavigateButton(true);
				} else {
					setShowNavigateButton(false);
				}
				setSnackbarOpen(true);
				setSnackbarMessage('Ping failed');
				setBackdropOpen(false);
				setMessageColor('error');
				setDialogMessage(error.message);
			});
	};

	const handleInstallUninstall = (install) => {
		setBackdropOpen(true);
		const encryptedUsername = encrypt(username);
		const encryptedPassword = encrypt(password);
		let hostsRaw = hosts.replace(/,|\s|\n/g, ',');
		hostsRaw = hostsRaw.replace(/,{2,}/g, ',').replace(/,$/, '');
		const encryptedHosts = encrypt(hostsRaw);

		const apiUrl = install ? '/api/target/install' : '/api/target/uninstall';
		fetch(window.location.origin + apiUrl, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({
				hosts: encryptedHosts,
				user: encryptedUsername,
				password: encryptedPassword,
				tags: selectedTags,
			}),
		})
			.then((response) => [response.json(), response.ok])
			.then(async (dataParam) => {
				const status = dataParam[1];
				const data = await dataParam[0];
				if (!status) {
					throw new Error(data.detail);
				}
				setShowNavigateButton(false);
				setSnackbarOpen(true);
				if (install) setSnackbarMessage('Install successful');
				else setSnackbarMessage('Uninstall successful');
				setBackdropOpen(false);
				setMessageColor('success');
				setDialogMessage(data);
			})
			.catch((error) => {
				setShowNavigateButton(false);
				setSnackbarOpen(true);
				if (install) setSnackbarMessage('Install failed');
				else setSnackbarMessage('Uninstall failed');
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
		<div
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
							onChange={(event) => {
								setUsername(event.target.value);
							}}
							value={username}
						/>
						<TextField
							id="password"
							required
							label="Password"
							size="small"
							type="password"
							variant="filled"
							fullWidth
							onChange={(event) => {
								setPassword(event.target.value);
							}}
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
							sx={{ width: '100%' }}
							maxRows={4}
							placeholder="Separated by commas, spaces or newlines"
							onChange={(event) => {
								handleHostsChange(event.target.value);
							}}
							value={hosts}
						/>
						<Autocomplete
							multiple
							id="tags-outlined"
							options={tags}
							getOptionLabel={(option) => option.title}
							filterSelectedOptions
							sx={{ maxWidth: '28vw', width: '100%' }}
							renderInput={(params) => (
								<TextField
									{...params} // eslint-disable-line react/jsx-props-no-spreading
									label="Select Software"
									placeholder="Select Software"
								/>
							)}
							onChange={(event, value) => {
								handleSoftwareListChange(value);
							}}
						/>
						<Grid item container>
							<Grid item margin={2} marginLeft={0}>
								<Button
									variant="contained"
									onClick={() => {
										handleInstallUninstall(true);
									}}
									color="success"
								>
									Install
								</Button>
							</Grid>
							<Grid item margin={2}>
								<Button
									variant="contained"
									onClick={() => {
										handleInstallUninstall(false);
									}}
									color="error"
								>
									Uninstall
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
				<a href="https://www.freepik.com/free-vector/it-professionals-are-creating-web-site-laptop-screen-illustration_10780362.htm?query=quick%20install%20webapp%20toolbox%20remote%20machine#from_view=detail_alsolike">
					Image by vectorjuice
				</a>{' '}
				on Freepik
			</Typography>
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
				<DialogTitle id="scroll-dialog-title">More Details</DialogTitle>
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
					{showNavigateButton ? (
						<Button
							onClick={() => {
								navigate('/configure-target');
							}}
							color="warning"
						>
							Configure Target
						</Button>
					) : null}
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
