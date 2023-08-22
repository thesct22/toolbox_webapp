import React, { useState, useEffect } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import InstallDesktopIcon from '@mui/icons-material/InstallDesktop';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import CodeIcon from '@mui/icons-material/Code';
import TerminalIcon from '@mui/icons-material/Terminal';
import InfoIcon from '@mui/icons-material/Info';
import SettingsIcon from '@mui/icons-material/Settings';
import Tooltip from '@mui/material/Tooltip';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function NavBar() {
	const navigate = useNavigate();

	const [windowWidth, setWindowWidth] = useState(window.innerWidth);

	// Update window width state on window resize
	const handleResize = () => {
		setWindowWidth(window.innerWidth);
	};

	useEffect(() => {
		window.addEventListener('resize', handleResize);

		// Clean up the event listener when the component unmounts
		return () => {
			window.removeEventListener('resize', handleResize);
		};
	}, []);

	const currentPage = useSelector((state) => state.currentPage);

	return (
		<Box sx={{ flexGrow: 1 }} id="navbar">
			<AppBar position="static">
				<Toolbar>
					<Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
						{currentPage.currentPage}
					</Typography>
					<Tooltip title="Installer: Use this page to quickly install the tools on your machine">
						{windowWidth < 1080 ? (
							<IconButton color="inherit" onClick={() => navigate('/')}>
								<InstallDesktopIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<InstallDesktopIcon />}
								onClick={() => navigate('/')}
							>
								Installer
							</Button>
						)}
					</Tooltip>
					<Tooltip title="Custom Playbook: Use this page to run custom playbooks">
						{windowWidth < 1080 ? (
							<IconButton
								color="inherit"
								onClick={() => navigate('/custom-playbook')}
							>
								<AutoStoriesIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<AutoStoriesIcon />}
								onClick={() => navigate('/custom-playbook')}
							>
								Custom Playbook
							</Button>
						)}
					</Tooltip>
					<Tooltip title="Configure Target: Use this page to configure the target(s) to be targeted by ansible">
						{windowWidth < 1080 ? (
							<IconButton
								color="inherit"
								onClick={() => navigate('/configure-target')}
							>
								<SettingsIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<SettingsIcon />}
								onClick={() => navigate('/configure-target')}
							>
								Configure Target
							</Button>
						)}
					</Tooltip>
					<Tooltip title="Code Editor: Use this page to edit the files you want to run ansible with">
						{windowWidth < 1080 ? (
							<IconButton
								color="inherit"
								onClick={() => navigate('/code-editor')}
							>
								<CodeIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<CodeIcon />}
								onClick={() => navigate('/code-editor')}
							>
								Code Editor
							</Button>
						)}
					</Tooltip>
					<Tooltip title="Terminal: Use this page to run bash commands on your machine/docker container">
						{windowWidth < 1080 ? (
							<IconButton color="inherit" onClick={() => navigate('/terminal')}>
								<TerminalIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<TerminalIcon />}
								onClick={() => navigate('/terminal')}
							>
								Terminal
							</Button>
						)}
					</Tooltip>
					<Tooltip title="Instructions: Use this page to learn how to use the tools">
						{windowWidth < 1080 ? (
							<IconButton
								color="inherit"
								onClick={() => navigate('/instructions')}
							>
								<InfoIcon />
							</IconButton>
						) : (
							<Button
								color="inherit"
								startIcon={<InfoIcon />}
								onClick={() => navigate('/instructions')}
							>
								Instructions
							</Button>
						)}
					</Tooltip>
				</Toolbar>
			</AppBar>
		</Box>
	);
}
