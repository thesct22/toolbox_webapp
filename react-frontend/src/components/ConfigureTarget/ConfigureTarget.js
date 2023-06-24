import React from 'react';
import { useDispatch, useSelector } from "react-redux";
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

export default function ConfigureTarget() {
	const dispatch = useDispatch();

	const [username, setUsername] = React.useState("");
	const [password, setPassword] = React.useState("");
	const [hosts, setHosts] = React.useState(useSelector((state) => state.hosts.hosts));
	const usernameChanged = (event) => {
			setUsername(event.target.value);
	}
	const passwordChanged = (event) => {
			setPassword(event.target.value);
	}

	const hostsChanged = (event) => {
			setHosts(event.target.value);
			dispatch({ type: "hosts/setHosts", payload: event.target.value });
	};
	
	const handleClick = () => {
		fetch(process.env.REACT_APP_API_URL + "/target/configure", {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				user: username,
				password: password,
				hosts: hosts,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error(response.statusText);
				}
				return response.json();
			})
			.then((data) => {
				console.log("Success:", data);
			})
			.catch((error) => {
				console.log("Error:", error.message);
			});
	};
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
						value={useSelector((state) => state.hosts.hosts)}	
					/>
				</Grid>
				<Grid item xs={12}>
					<Button
							onClick={handleClick}
					>
							Configure
					</Button>
				</Grid>
			</Grid>
		</div>
	);
}