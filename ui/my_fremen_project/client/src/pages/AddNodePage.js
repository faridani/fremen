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
