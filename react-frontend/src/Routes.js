import React from 'react';
import { Routes as DomRoutes, Route } from 'react-router-dom';

import Home from './components/Home/Home';
import CodeEditor from './components/CodeEditor/CodeEditor';
import Terminal from './components/Terminal/Terminal';
import Instructions from './components/Instructions/Instructions';

function Routes() {


  return (
    <DomRoutes>
      <Route path="/" element={<Home />} />
      <Route path="/code-editor" element={<CodeEditor />} />
      <Route path="/terminal" element={<Terminal />} />
      <Route path="/instructions" element={<Instructions />} />
    </DomRoutes>
  );
}

export default Routes;
