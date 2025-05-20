// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import WorkflowPage from './pages/WorkflowPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AddNodePage from './pages/AddNodePage';

function App() {
  return (
    <Router>
      <div>
        {/* Simple top nav */}
        <nav style={{ padding: '10px', backgroundColor: '#eee', marginBottom: '10px' }}>
          <Link to="/" style={{ marginRight: 10 }}>Workflows</Link>
          <Link to="/addnode" style={{ marginRight: 10 }}>Add Node</Link>
          <Link to="/login" style={{ marginRight: 10 }}>Login</Link>
          <Link to="/register" style={{ marginRight: 10 }}>Register</Link>
        </nav>

        <Routes>
          <Route path="/" element={<WorkflowPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* <-- Our new route for creating node types --> */}
          <Route path="/addnode" element={<AddNodePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
