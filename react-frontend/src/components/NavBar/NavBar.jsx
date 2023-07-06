import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import InstallDesktopIcon from '@mui/icons-material/InstallDesktop';
import CodeIcon from '@mui/icons-material/Code';
import TerminalIcon from '@mui/icons-material/Terminal';
import InfoIcon from '@mui/icons-material/Info';
import SettingsIcon from '@mui/icons-material/Settings';
import Tooltip from '@mui/material/Tooltip';
import { useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function NavBar() {
	const navigate = useNavigate();

	const currentPage = useSelector((state) => state.currentPage);

	return (
		<Box sx={{ flexGrow: 1 }}>
			<AppBar position="static">
				<Toolbar>
					<Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
						{currentPage.currentPage}
					</Typography>
					<Tooltip title="Installer">
						<IconButton color="inherit" onClick={() => navigate('/')}>
							<InstallDesktopIcon />
						</IconButton>
					</Tooltip>
					<Tooltip title="Configure Target">
						<IconButton
							color="inherit"
							onClick={() => navigate('/configure-target')}
						>
							<SettingsIcon />
						</IconButton>
					</Tooltip>
					<Tooltip title="Code Editor">
						<IconButton
							color="inherit"
							onClick={() => navigate('/code-editor')}
						>
							<CodeIcon />
						</IconButton>
					</Tooltip>
					<Tooltip title="Terminal">
						<IconButton color="inherit" onClick={() => navigate('/terminal')}>
							<TerminalIcon />
						</IconButton>
					</Tooltip>
					<Tooltip title="Instructions">
						<IconButton
							color="inherit"
							onClick={() => navigate('/instructions')}
						>
							<InfoIcon />
						</IconButton>
					</Tooltip>
				</Toolbar>
			</AppBar>
		</Box>
	);
}
