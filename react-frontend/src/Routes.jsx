import React from 'react';
import { Routes as DomRoutes, Route } from 'react-router-dom';

import Home from './components/Home/Home';
import ConfigureTarget from './components/ConfigureTarget/ConfigureTarget';
import CodeEditor from './components/CodeEditor/CodeEditor';
import CustomPlaybook from './components/CustomPlaybook/CustomPlaybook';
import Terminal from './components/Terminal/Terminal';
import Instructions from './components/Instructions/Instructions';

function Routes() {
	return (
		<DomRoutes>
			<Route path="/" element={<Home />} />
			<Route path="/custom-playbook" element={<CustomPlaybook />} />
			<Route path="/configure-target" element={<ConfigureTarget />} />
			<Route path="/code-editor" element={<CodeEditor />} />
			<Route path="/terminal" element={<Terminal />} />
			<Route path="/instructions" element={<Instructions />} />
		</DomRoutes>
	);
}

export default Routes;
