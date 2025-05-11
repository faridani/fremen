# Project Documentation

Generated on: 2024-12-30 20:07:58


file path: client\Dockerfile

```
FROM node:18-alpine

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

COPY . .
CMD ["yarn", "start"]

```
file path: client\package.json

```json
{
  "name": "client",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@xyflow/react": "12",
    "axios": "^1.7.9",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "react-router-dom": "^7.1.1",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": "react-app"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

```
file path: client\public\index.html

```html
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width" />
		<meta name="theme-color" content="#000000" />
		<meta name="description" content="My description" />
		<title>React App</title>

		<link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
		<link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
		<link rel="manifest" href="%PUBLIC_URL%/manifest.json" />

		<!-- CSS & Icons -->
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" />
		<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
		<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
	</head>
	<body>
		<noscript>You need to enable JavaScript to run this app.</noscript>
		<div id="root"></div>

		<!-- jQuery first, then Popper.js, then Bootstrap JS -->
		<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js"></script>
		<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
	</body>
</html>

```
file path: client\public\manifest.json

```json
{
  "short_name": "React App",
  "name": "Create React App Sample",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}

```
file path: client\public\robots.txt

```
# https://www.robotstxt.org/robotstxt.html
User-agent: *

```
file path: client\README.md

```markdown
# [Create React App] Basic Template

## Commands

### Update the template

```npm publish```

#### Remember to change the version in the package.json

### Use the template

```npx create-react-app my-app --template basic```

```
file path: client\src\App.js

```javascript
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

```
file path: client\src\components\NodeTypeCreator.js

```javascript

import React, { useState } from 'react';
import { createNodeType } from '../utils/api';

export default function NodeTypeCreator({ onCreate }) {
  const [name, setName] = useState('');
  const [code, setCode] = useState(`def run(inputs, config):\n    return None`);
  const [isPublic, setIsPublic] = useState(false);

  const handleCreate = async () => {
    if (!name.trim()) {
      alert('Please enter a name for the node type.');
      return;
    }

    try {
      await createNodeType(name, code, isPublic);
      alert('Node type created successfully!');
      // Clear form
      setName('');
      setCode(`def run(inputs, config):\n    return None`);
      setIsPublic(false);
      // Notify parent so it can refresh the node list
      if (onCreate) onCreate();
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || 'Failed to create node type');
    }
  };

  return (
    <div style={{ margin: '20px 0' }}>
      <h3>Add a New Node Type</h3>

      <div style={{ marginBottom: 10 }}>
        <label>Name:</label>
        <br />
        <input
          style={{ width: '100%' }}
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>Code (Python `run` function):</label>
        <br />
        <textarea
          rows={6}
          style={{ width: '100%' }}
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 10 }}>
        <label>
          <input
            type="checkbox"
            checked={isPublic}
            onChange={(e) => setIsPublic(e.target.checked)}
          />
          &nbsp;Make this node type public?
        </label>
      </div>

      <button onClick={handleCreate}>Create Node Type</button>
    </div>
  );
}
```
file path: client\src\index.css

```css
body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

```
file path: client\src\index.js

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

```
file path: client\src\pages\AddNodePage.js

```javascript
// src/pages/AddNodePage.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

import NodeTypeCreator from '../components/NodeTypeCreator';
import { fetchNodeTypes } from '../utils/api';

export default function AddNodePage() {
  const [nodeTypes, setNodeTypes] = useState([]);

  // Load node types on mount
  useEffect(() => {
    loadNodeTypes();
  }, []);

  const loadNodeTypes = async () => {
    try {
      const res = await fetchNodeTypes();
      setNodeTypes(res.data);
    } catch (err) {
      console.error('Failed to fetch node types:', err);
      alert('Failed to fetch node types');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Node Library Manager</h2>
      <p>
        <Link to="/">← Back to Workflows</Link>
      </p>

      {/* The form for creating a new node type */}
      <NodeTypeCreator onCreate={loadNodeTypes} />

      {/* Display the existing node types */}
      <h3>Existing Node Types</h3>
      {nodeTypes.length === 0 ? (
        <p>No node types found.</p>
      ) : (
        <ul>
          {nodeTypes.map((nt) => (
            <li key={nt.id} style={{ marginBottom: 5 }}>
              <strong>{nt.name}</strong>
              {nt.is_public ? ' (Public)' : ' (Private)'}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

```
file path: client\src\pages\LoginPage.js

```javascript
import React, { useState } from 'react';
import { loginUser } from '../utils/api';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(username, password);
      alert(res.data.message);
    } catch (err) {
      alert(err.response.data.error || 'Error logging in');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label><br />
          <input value={username} onChange={e => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password:</label><br />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div><br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;

```
file path: client\src\pages\RegisterPage.js

```javascript
import React, { useState } from 'react';
import { registerUser } from '../utils/api';

const RegisterPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await registerUser(username, password);
      alert(res.data.message);
    } catch (err) {
      alert(err.response.data.error || 'Error registering');
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Register</h2>
      <form onSubmit={handleRegister}>
        <div>
          <label>Username:</label><br />
          <input value={username} onChange={e => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password:</label><br />
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div><br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;

```
file path: client\src\pages\WorkflowPage.js

```javascript
import React, { useState, useEffect, useCallback } from 'react';
// React Flow imports
import {
  ReactFlowProvider,
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import {
  fetchWorkflows,
  createWorkflow,
  getWorkflowDetail,
  updateWorkflow,
  runWorkflow,
  fetchNodeTypes
} from '../utils/api';

function NodeLibraryPanel({ nodeTypes }) {
  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify(nodeType));
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div style={{ padding: '10px', borderTop: '1px solid #ccc', marginTop: '10px' }}>
      <h4>Node Library</h4>
      {nodeTypes.map((nt) => (
        <div
          key={nt.id}
          draggable
          onDragStart={(event) => onDragStart(event, nt)}
          style={{
            border: '1px solid #ccc',
            margin: '5px 0',
            padding: '5px',
            cursor: 'grab',
            backgroundColor: '#fff'
          }}
        >
          {nt.name}
          {nt.is_public ? ' (public)' : ''}
        </div>
      ))}
    </div>
  );
}

function DragDropWorkflowUI() {
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [workflowName, setWorkflowName] = useState('');
  const [isPublic, setIsPublic] = useState(false);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowInstance = useReactFlow();

  const [nodeTypes, setNodeTypes] = useState([]);

  useEffect(() => {
    loadWorkflows();
    loadNodeTypes();
  }, []);

  const loadWorkflows = async () => {
    try {
      const res = await fetchWorkflows();
      setWorkflows(res.data);
    } catch (err) {
      console.error('Failed to fetch workflows:', err);
      alert('Failed to fetch workflows');
    }
  };

  const loadNodeTypes = async () => {
    try {
      const res = await fetchNodeTypes();
      setNodeTypes(res.data);
    } catch (err) {
      console.error('Failed to fetch node types:', err);
      alert('Failed to fetch node types');
    }
  };

  const handleCreateWorkflow = async () => {
    try {
      await createWorkflow(workflowName, isPublic);
      alert('Workflow created!');
      setWorkflowName('');
      setIsPublic(false);
      loadWorkflows();
    } catch (err) {
      alert(err.response?.data?.error || 'Error creating workflow');
    }
  };

  const handleSelectWorkflow = async (wf) => {
    setSelectedWorkflow(wf);

    try {
      const detailRes = await getWorkflowDetail(wf.id);
      const wfDetail = detailRes.data;

      const rfNodes = wfDetail.nodes.map((n) => ({
        id: n.id.toString(),
        position: { x: n.position.x, y: n.position.y },
        data: {
          label: `Node ${n.id}`,
          nodeTypeId: n.node_type_id,
          config: n.config
        },
        style: {
          width: n.size.width || 200,
          height: n.size.height || 100
        }
      }));

      const rfEdges = wfDetail.edges.map((e) => ({
        id: e.id.toString(),
        source: e.source.toString(),
        target: e.target.toString(),
        label: e.label
      }));

      setNodes(rfNodes);
      setEdges(rfEdges);
    } catch (err) {
      console.error('Failed to load workflow detail:', err);
      alert('Failed to load workflow detail');
    }
  };

  const handleSaveWorkflow = async () => {
    if (!selectedWorkflow) return;

    const backendNodes = nodes.map((n) => ({
      node_type_id: n.data.nodeTypeId || null,
      position: { x: n.position.x, y: n.position.y },
      size: { width: n.style?.width || 200, height: n.style?.height || 100 },
      config: n.data.config || ''
    }));

    const backendEdges = edges.map((e) => ({
      source: parseInt(e.source),
      target: parseInt(e.target),
      label: e.label || ''
    }));

    const payload = {
      name: selectedWorkflow.name,
      is_public: selectedWorkflow.is_public,
      nodes: backendNodes,
      edges: backendEdges
    };

    try {
      await updateWorkflow(selectedWorkflow.id, payload);
      alert('Workflow saved');
      loadWorkflows();
    } catch (err) {
      console.error('Failed to save workflow:', err);
      alert('Failed to save workflow');
    }
  };

  const handleRunWorkflow = async () => {
    if (!selectedWorkflow) return;
    try {
      const res = await runWorkflow(selectedWorkflow.id);
      console.log('Workflow run result:', res.data);
      alert('Workflow executed. Check console for output.');
    } catch (err) {
      console.error('Failed to run workflow:', err);
      alert('Failed to run workflow');
    }
  };

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const droppedData = event.dataTransfer.getData('application/reactflow');
      if (!droppedData) return;

      const nodeType = JSON.parse(droppedData);
      const position = reactFlowInstance.project({ x: event.clientX, y: event.clientY });

      const newNode = {
        id: `dndnode_${Date.now()}`,
        position,
        data: {
          label: nodeType.name,
          nodeTypeId: nodeType.id
        },
        style: { width: 200, height: 100 }
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  return (
    <div style={{ display: 'flex' }}>
      <div style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px' }}>
        <h3>Create Workflow</h3>
        <div>
          <input
            style={{ width: '100%' }}
            placeholder="Workflow Name"
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
          />
          <div>
            <label>
              <input
                type="checkbox"
                checked={isPublic}
                onChange={(e) => setIsPublic(e.target.checked)}
              />
              Public
            </label>
            <button onClick={handleCreateWorkflow}>Create</button>
          </div>
        </div>

        <h3>Workflows</h3>
        <ul>
          {workflows.map((wf) => (
            <li
              key={wf.id}
              style={{ cursor: 'pointer' }}
              onClick={() => handleSelectWorkflow(wf)}
            >
              {wf.name} {wf.is_public ? '(public)' : ''}
            </li>
          ))}
        </ul>

        {selectedWorkflow && (
          <>
            <h3>Selected: {selectedWorkflow.name}</h3>
            <button onClick={handleSaveWorkflow}>Save</button>
            <button onClick={handleRunWorkflow}>Run</button>
          </>
        )}

        <NodeLibraryPanel nodeTypes={nodeTypes} />
      </div>

      <div style={{ flex: 1, height: '100vh' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onDragOver={onDragOver}
          onDrop={onDrop}
          fitView
        >
          <MiniMap />
          <Controls />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}

export default function WorkflowPage() {
  return (
    <ReactFlowProvider>
      <DragDropWorkflowUI />
    </ReactFlowProvider>
  );
}

```
file path: client\src\utils\api.js

```javascript
import axios from 'axios';

// In development, you might set this to http://localhost:5000
// Or have a proxy in package.json
const API_BASE = 'http://localhost:5000/api';

export const registerUser = (username, password) => {
  return axios.post(`${API_BASE}/register`, { username, password }, { withCredentials: true });
};

export const loginUser = (username, password) => {
  return axios.post(`${API_BASE}/login`, { username, password }, { withCredentials: true });
};

export const logoutUser = () => {
  return axios.post(`${API_BASE}/logout`, {}, { withCredentials: true });
};

export const fetchWorkflows = () => {
  return axios.get(`${API_BASE}/workflows`, { withCredentials: true });
};

export const createWorkflow = (name, is_public) => {
  return axios.post(`${API_BASE}/workflows`, { name, is_public }, { withCredentials: true });
};

export const getWorkflowDetail = (workflow_id) => {
  return axios.get(`${API_BASE}/workflows/${workflow_id}`, { withCredentials: true });
};

export const updateWorkflow = (workflow_id, payload) => {
  return axios.put(`${API_BASE}/workflows/${workflow_id}`, payload, { withCredentials: true });
};

export const runWorkflow = (workflow_id) => {
  return axios.post(`${API_BASE}/workflows/${workflow_id}/run`, {}, { withCredentials: true });
};

export const fetchNodeTypes = () => {
  return axios.get(`${API_BASE}/node_types`, { withCredentials: true });
};

export const createNodeType = (name, code, is_public) => {
  return axios.post(`${API_BASE}/node_types`, { name, code, is_public }, { withCredentials: true });
};

```
file path: docker-compose.yml

```yaml
version: "3.9"

services:
  server:
    build: ./server
    container_name: fremen_flask_server
    ports:
      - "5000:5000"
    volumes:
      - ./server:/app
    depends_on:
      - client

  client:
    build: ./client
    container_name: fremen_react_client
    ports:
      - "3000:3000"
    volumes:
      - ./client:/app

```
file path: prompt.txt

```

```
file path: server\__init__.py

```python

```
file path: server\auth_routes.py

```python
"""
auth_routes.py
Routes for user registration, login, and logout.
"""

from flask import Blueprint, request, jsonify, session
from passlib.hash import pbkdf2_sha256
from database import db
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password
    password_hash = pbkdf2_sha256.hash(password)
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not pbkdf2_sha256.verify(password, user.password_hash):
        return jsonify({"error": "Invalid password"}), 401

    # Store user info in session
    session["user_id"] = user.id
    return jsonify({"message": "Login successful", "user_id": user.id}), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200

```
file path: server\config.py

```python
"""
config.py
Configuration settings for the Flask application.
"""

import os

# You can set SECRET_KEY to something random in production
SECRET_KEY = os.environ.get("SECRET_KEY", "mysecretkey")

# SQLite database file (local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False

```
file path: server\database.py

```python
"""
database.py
Sets up the SQLAlchemy database connection and session.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

```
file path: server\Dockerfile

```
# Use Python 3.12 slim as the base
FROM python:3.12-slim

# Create the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Command to run
CMD ["python", "main.py"]

```
file path: server\function_registry.py

```python
"""
function_registry.py
Stores and compiles user-defined functions from NodeType.
We can dynamically exec the code in a safe(ish) environment for demonstration.
In a real project, you'd want more security measures.
"""

import types

def compile_node_type_code(code_string):
    """
    Given a code string, compile it into a callable Python function object.
    We expect the code_string to define a function named 'run' or similar.
    This is extremely simplified for demonstration purposes.
    """
    # We'll use a dict as the local namespace for exec
    local_namespace = {}
    exec(code_string, {}, local_namespace)
    # We expect a function named 'run' in local_namespace
    func = local_namespace.get("run", None)
    if func is None or not isinstance(func, types.FunctionType):
        raise ValueError("No 'run' function found in the code")
    return func

```
file path: server\main.py

```python
"""
main.py
Entry point to run the Flask application.
"""

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import session
from flask import g
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from models import *  # import all models so they are registered
from auth_routes import auth_bp
from node_routes import node_bp
from workflow_routes import workflow_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    # Initialize database
    db.init_app(app)

    # Enable CORS for all endpoints
    CORS(app, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(node_bp, url_prefix="/api")
    app.register_blueprint(workflow_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

```
file path: server\models.py

```python
"""
models.py
Defines our database models using SQLAlchemy.
"""

from datetime import datetime
from database import db

# Association of Users, Workflows, and Node types, etc.

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Relationship - a user has many workflows
    workflows = db.relationship("Workflow", back_populates="owner")

    # Relationship - a user has many node types
    node_types = db.relationship("NodeType", back_populates="owner")

class NodeType(db.Model):
    """
    NodeType holds custom Python code, function name, etc.
    If is_public=False, only the owner can use it.
    """
    __tablename__ = "node_types"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.Text, nullable=False)      # The Python function code
    is_public = db.Column(db.Boolean, default=False)

    # Relationship back to user
    owner = db.relationship("User", back_populates="node_types")

class Workflow(db.Model):
    """
    Workflow represents a DAG. 
    If is_public=False, only the owner can see it.
    """
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_public = db.Column(db.Boolean, default=False)

    # Relationship back to user
    owner = db.relationship("User", back_populates="workflows")

    # A workflow has many nodes
    nodes = db.relationship("WorkflowNode", back_populates="workflow", cascade="all, delete-orphan")
    # A workflow has many edges
    edges = db.relationship("WorkflowEdge", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowNode(db.Model):
    """
    A node in a workflow. Each node references a NodeType for its behavior.
    config can store JSON of custom parameters.
    """
    __tablename__ = "workflow_nodes"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    node_type_id = db.Column(db.Integer, db.ForeignKey("node_types.id"), nullable=True)
    x = db.Column(db.Float, default=0.0)
    y = db.Column(db.Float, default=0.0)
    width = db.Column(db.Float, default=200.0)
    height = db.Column(db.Float, default=100.0)
    config = db.Column(db.Text, nullable=True)  # JSON or other text

    # Relationship
    workflow = db.relationship("Workflow", back_populates="nodes")

class WorkflowEdge(db.Model):
    """
    An edge in a workflow. Possibly carry a label to support conditional logic.
    """
    __tablename__ = "workflow_edges"

    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey("workflows.id"), nullable=False)
    source_node_id = db.Column(db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False)
    target_node_id = db.Column(db.Integer, db.ForeignKey("workflow_nodes.id"), nullable=False)
    label = db.Column(db.String(50), nullable=True)

    # Relationship
    workflow = db.relationship("Workflow", back_populates="edges")

```
file path: server\node_routes.py

```python
"""
node_routes.py
Routes related to NodeTypes (creating new node types, listing them, etc.)
"""

from flask import Blueprint, request, jsonify, session
from database import db
from models import User, NodeType

node_bp = Blueprint("nodes", __name__)

@node_bp.route("/node_types", methods=["GET"])
def get_node_types():
    """
    Get the list of node types accessible to the current user:
    - All public node types
    - The user's private node types
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    # All public node types
    public_node_types = NodeType.query.filter_by(is_public=True).all()
    # The user's private node types
    private_node_types = NodeType.query.filter_by(user_id=user_id, is_public=False).all()

    # Combine
    result = []
    for nt in public_node_types + private_node_types:
        result.append({
            "id": nt.id,
            "name": nt.name,
            "is_public": nt.is_public
        })

    return jsonify(result), 200

@node_bp.route("/node_types", methods=["POST"])
def create_node_type():
    """
    Create a new NodeType (function) for the current user.
    Body should contain: name, code, is_public
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    code = data.get("code")
    is_public = data.get("is_public", False)

    if not name or not code:
        return jsonify({"error": "Missing name or code"}), 400

    # Create new node type
    node_type = NodeType(user_id=user_id, name=name, code=code, is_public=is_public)
    db.session.add(node_type)
    db.session.commit()

    return jsonify({"message": "Node type created", "node_type_id": node_type.id}), 201

```
file path: server\requirements.txt

```
flask==2.2.5
flask_sqlalchemy==3.0.5
flask_cors==3.0.10
PyJWT==2.8.0
passlib==1.7.4
networkx==3.1

```
file path: server\workflow_executor.py

```python
"""
workflow_executor.py
Contains logic to topologically sort a workflow's nodes and execute them
in the correct sequence.
Also supports conditional branching and sub-workflows if needed.
"""

import networkx as nx
import json
from function_registry import compile_node_type_code
from models import WorkflowNode, WorkflowEdge, NodeType, Workflow, db

def execute_workflow(workflow):
    """
    1. Build a directed graph with networkx.
    2. Topologically sort the nodes.
    3. For each node, retrieve the Python function (node_type code), run it,
       pass in inputs from the edges that led to this node.
    4. If the node returns a labeled output, follow the correct edges, etc.
    5. Return the final outputs or intermediate results as desired.
    """
    G = nx.DiGraph()

    # Add nodes
    for node in workflow.nodes:
        G.add_node(node.id, node_obj=node)

    # Add edges with label
    for edge in workflow.edges:
        G.add_edge(edge.source_node_id, edge.target_node_id, label=edge.label)

    # We'll do a simple topological sort for demonstration
    # However, note that conditional branching can skip nodes
    # In a real scenario you'd do a BFS or DFS that only follows the chosen edges
    try:
        sorted_nodes = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible as e:
        raise Exception("Cyclic dependency detected in the workflow") from e

    # We'll store the output of each node in a dictionary
    node_outputs = {}

    for node_id in sorted_nodes:
        node_data = G.nodes[node_id]["node_obj"]
        if not node_data.node_type_id:
            # This might be a subworkflow reference or something else
            # For now, let's skip or handle subworkflow logic
            node_outputs[node_id] = None
            continue

        node_type = NodeType.query.get(node_data.node_type_id)
        # Compile code
        func = compile_node_type_code(node_type.code)

        # Gather inputs from predecessor edges
        inputs = []
        pred_nodes = G.predecessors(node_id)
        for pn in pred_nodes:
            edge_data = G.get_edge_data(pn, node_id)
            # If the predecessor node had multiple outputs with labels, we might match by label.
            # For demonstration, just store the entire predecessor's output for now.
            inputs.append(node_outputs.get(pn, None))

        # If node_data.config is JSON, parse it
        config = {}
        if node_data.config:
            try:
                config = json.loads(node_data.config)
            except:
                pass

        # Call the function
        # For demonstration, let's assume the function signature is run(inputs, config)
        # The user can define it as they see fit.
        result = func(inputs, config)
        node_outputs[node_id] = result

    # For demonstration, return all node_outputs
    return node_outputs

```
file path: server\workflow_routes.py

```python
"""
workflow_routes.py
Handles creation, update, retrieval, and execution of workflows (DAGs).
"""

from flask import Blueprint, request, jsonify, session
from database import db
from models import User, Workflow, WorkflowNode, WorkflowEdge, NodeType
from workflow_executor import execute_workflow

workflow_bp = Blueprint("workflows", __name__)

@workflow_bp.route("/workflows", methods=["GET"])
def get_workflows():
    """
    Return a list of workflows the user can see:
    - All public workflows
    - The user's private workflows
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    public_wfs = Workflow.query.filter_by(is_public=True).all()
    private_wfs = Workflow.query.filter_by(user_id=user_id, is_public=False).all()

    result = []
    for wf in public_wfs + private_wfs:
        result.append({
            "id": wf.id,
            "name": wf.name,
            "is_public": wf.is_public
        })

    return jsonify(result), 200

@workflow_bp.route("/workflows", methods=["POST"])
def create_workflow():
    """
    Create a new workflow with an initial name and visibility.
    Request body: { name, is_public }
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get("name")
    is_public = data.get("is_public", False)

    if not name:
        return jsonify({"error": "Missing workflow name"}), 400

    wf = Workflow(user_id=user_id, name=name, is_public=is_public)
    db.session.add(wf)
    db.session.commit()

    return jsonify({"message": "Workflow created", "workflow_id": wf.id}), 201

@workflow_bp.route("/workflows/<int:workflow_id>", methods=["GET"])
def get_workflow_detail(workflow_id):
    """
    Get the details (nodes, edges) of a workflow if the user has access.
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership or public
    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    nodes = []
    for node in wf.nodes:
        nodes.append({
            "id": node.id,
            "node_type_id": node.node_type_id,
            "position": {"x": node.x, "y": node.y},
            "size": {"width": node.width, "height": node.height},
            "config": node.config
        })

    edges = []
    for edge in wf.edges:
        edges.append({
            "id": edge.id,
            "source": edge.source_node_id,
            "target": edge.target_node_id,
            "label": edge.label
        })

    return jsonify({
        "id": wf.id,
        "name": wf.name,
        "is_public": wf.is_public,
        "nodes": nodes,
        "edges": edges
    }), 200

@workflow_bp.route("/workflows/<int:workflow_id>", methods=["PUT"])
def update_workflow(workflow_id):
    """
    Update the workflow's name, visibility, nodes, and edges.
    Expect the front-end to send { name, is_public, nodes[], edges[] } to save.
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership
    if wf.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    wf.name = data.get("name", wf.name)
    wf.is_public = data.get("is_public", wf.is_public)

    # Clear existing nodes/edges and recreate them
    WorkflowNode.query.filter_by(workflow_id=wf.id).delete()
    WorkflowEdge.query.filter_by(workflow_id=wf.id).delete()

    # Create new nodes
    nodes_data = data.get("nodes", [])
    for nd in nodes_data:
        # node_type_id might be null if it's a sub-workflow reference or something
        node = WorkflowNode(
            workflow_id=wf.id,
            node_type_id=nd.get("node_type_id"),
            x=nd["position"]["x"],
            y=nd["position"]["y"],
            width=nd["size"]["width"],
            height=nd["size"]["height"],
            config=nd.get("config", "")
        )
        db.session.add(node)
        db.session.flush()  # to get an ID

    db.session.commit()

    # We have to re-fetch the nodes we just created to properly map IDs
    # In a real app, you'd handle ID mapping carefully. For simplicity, we assume
    # that the front end doesn't need consistent IDs across updates.
    # For a demonstration, let's just store edges referencing the new node IDs if needed.

    # Create new edges
    edges_data = data.get("edges", [])
    for ed in edges_data:
        edge = WorkflowEdge(
            workflow_id=wf.id,
            source_node_id=ed["source"],
            target_node_id=ed["target"],
            label=ed.get("label", "")
        )
        db.session.add(edge)

    db.session.commit()

    return jsonify({"message": "Workflow updated"}), 200

@workflow_bp.route("/workflows/<int:workflow_id>/run", methods=["POST"])
def run_workflow(workflow_id):
    """
    Execute the workflow DAG in topological order using networkx, etc.
    The user must have access to the workflow (own it or it's public).
    """
    user_id = session.get("user_id", None)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    wf = Workflow.query.filter_by(id=workflow_id).first()
    if not wf:
        return jsonify({"error": "Workflow not found"}), 404

    # Check ownership or public
    if (wf.user_id != user_id) and (not wf.is_public):
        return jsonify({"error": "Forbidden"}), 403

    # Execute
    try:
        execution_result = execute_workflow(wf)
        return jsonify({"status": "success", "result": execution_result}), 200
    except Exception as e:
        return jsonify({"status": "failure", "error": str(e)}), 500

```