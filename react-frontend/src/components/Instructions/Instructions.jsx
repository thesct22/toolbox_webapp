import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import Navbar from './NavBar.jpg'
import Installer from './Installer.jpg'
import CustomPlaybook from './CustomPlaybook.jpg'
import ConfigureTarget from './ConfigureTarget.jpg'
import CodeEditor from './CodeEditor.jpg'
import Terminal from './Terminal.jpg'

export default function Instructions() {
	const dispatch = useDispatch();

	useEffect(() => {
		dispatch({ type: 'currentPage/setCurrentPage', payload: 'Instructions' });
	}, []);

	return (
		<div style={{ textAlign: 'left', padding: '2rem' }}>
		<h2 id="navigation-bar">Navigation bar</h2>
		<p><img src={Navbar} style={{ width: '75%', height: 'auto' }} alt="Navbar"/></p>
		<ol>
		  <li>Installer Page <code> &apos;/&apos;</code>as a quick configuration page</li>
		  <li>Custom Playbook Page <code>&apos;/custom-playbook&apos;</code> to construct the commands to run</li>
		  <li>Configure Target Page <code>&apos;/configure-target&apos;</code> to configure the target machines</li>
		  <li>Code Editor Page <code>&apos;/code-editor&apos;</code> to edit the files as per your need.</li>
		  <li>Terminal Page <code>&apos;/terminal&apos;</code> gives you access to a bash shell inside the container as root user.</li>
		  <li>This Instructions Section<code>&apos;/help&apos;</code>.</li>
  
		</ol>
		<h2 id="installer-page">Installer Page</h2>
		<p><img src={Installer} style={{ width: '75%', height: 'auto' }} alt="Installer Page"/></p>
		<ol>
		  <li>Here you can specify the device name () or IP address of all the machines you wish ansible to configure, seperated by commas.</li>
		  <li>Specify the username and password of the user you wish ansible to use to connect to the machines.</li>
		  <li>Select the software you wish to install/uninstall using the multi-select option.</li>
		  <li>Click on the <code>Install</code> button to install the selected software.</li>
		  <li>Click on the <code>Uninstall</code> button to uninstall the selected software.</li>
		  <li>Click the <code>Ping</code> button to ping the machines and see if they are reachable.</li>
		  <li>The installation takes time, so be patient and refrain from clicking refresh or back button.</li>
		  <li>Once the process is complete, you will be receive the success or failure message.</li>
		  <li>Click on the <code>More Details</code> button on the pop up to see the details of the run in a Dialog box.</li>
		</ol>
		<h2 id="custom-playbook-page">Custom Playbook Page</h2>
		<p><img src={CustomPlaybook} style={{ width: '75%', height: 'auto' }} alt='Custom Playbook Page'/></p>
		<ol>
		  <li>This page is meant to be used by advanced users who wish to construct and run custom playbooks.</li>
		  <li>Use the explorer on the left to click the playbook yaml files and hosts files (preview available as well)</li>
		  <li>Specify the username and password of the user you wish ansible to use to connect to the machines.</li>
		  <li>Choose the tags you wish to run.</li>
		  <li>Add the level of verbosity you wish.</li>
		  <li>Pass additional arguments to your command as needed.</li>
		  <li>Add any variables you need to pass to the playbook.</li>
		  <li>This list generates a new key:value input pair every time you enter something on the last variables pair.</li>
		  <li>Once you finalize your command, press &quot;Run&quot;</li>
		  <li>Click the <code>Ping</code> button to ping the machines and see if they are reachable.</li>
		  <li>The installation takes time, so be patient and refrain from clicking refresh or back button.</li>
		  <li>Once the process is complete, you will be receive the success or failure message.</li>
		  <li>Click on the <code>More Details</code> button on the pop up to see the details of the run in a Dialog box.</li>
		</ol>
		<h2 id="configure-target-page">Configure Target Page</h2>
		<p><img src={ConfigureTarget} style={{ width: '75%', height: 'auto' }} alt='Configure Target Page'/></p>
		<ol>
		  <li>This page is used to configure the target machines to be accessible to the toolbox.</li>
		  <li>This process needs to be done only once for a target machine.</li>
		  <li>Once configured, the toolbox can be used to run any commands on the target machine without any further configuration in later runs.</li>
		  <li>Here you can specify the device name () or IP address of all the machines you wish to configure to be accessible by this toolbox, seperated by commas.</li>
		  <li>Specify the username and password of the user you wish ansible to use to connect to the machines.</li>
		  <li>Click the <code>Configure</code> button to configure the target machines.</li>
		</ol>
		<h2 id="code-editor-page">Code Editor Page</h2>
		<p><img src={CodeEditor} style={{ width: '75%', height: 'auto' }} alt='Code Editor Page'/></p>
		<ol>
		  <li>Use the explorer on the left to access files you wish to edit.</li>
		  <li>Once you click, the file is loaded on the editor to the right.</li>
		  <li>Use the &quot;Choose Language&quot; option to choose the langauge of the file you are editing if you like some formatting.</li>
		  <li>The code editor is configured to automatically select the right formatting for you.</li>
		  <li>click &quot;Save&quot; to save the file and &quot;Reset&quot; to discard the changes.</li>
		  <li>Undo and Redo is enabled (Ctrl+Z, Ctrl+Y).</li>
		  <li>⚠️ If you undo after loading a file, the content on editor will be replaced by previously opened file&#39;s content. If you press &quot;Save&quot; this will be saved to the new file. Use with caution.</li>
		  <li>You can add, delete and rename files and folders using the file explorer on the left.</li>
		  <li>Right click on a file you wish to delete or rename.</li>
		  <li>Right click on a folder to add new files or folders inside that folder or delete and rename it.</li>
		  <li>Ansible is the root folder and this can be right clicked to add files and folders to it.</li>
		</ol>
		<h2 id="terminal-page">Terminal page</h2>
		<p><img src={Terminal} style={{ width: '75%', height: 'auto' }} alt='Terminal'/></p>
		<ol>
		  <li>This page is meant to be used by advanced users who wish to run commands on the terminal. Do not play around if you do not know much about the consequences.</li>
		  <li>The terminal can also be used to run any commands you wish to.</li>
		  <li>⚠️ It runs as <code>ansible</code> user with sudo privileges available to it(inside the container).⚠️</li>
		  <li>⚠️ Take care while working on the terminal page as the executable and dev versions have access to your local machine&apos;s terminal and this can have unforseen consequences. ⚠️</li>
		</ol>
  
	  </div>
	);
}
