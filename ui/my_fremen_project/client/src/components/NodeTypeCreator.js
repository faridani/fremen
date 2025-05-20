
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