// src/pages/WorkflowPage.js
import React, { useState, useEffect, useCallback } from 'react';
import {
  ReactFlowProvider,
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
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

// NodeLibraryPanel component remains the same
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

// Main workflow component with ReactFlow
function WorkflowContent() {
  const [workflows, setWorkflows] = useState([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);
  const [workflowName, setWorkflowName] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [nodeTypes, setNodeTypes] = useState([]);
  
  // Get the ReactFlow instance
  const reactFlowInstance = useReactFlow();

  useEffect(() => {
    loadWorkflows();
    loadNodeTypes();
  }, []);

  // Load workflows and node types functions remain the same
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

  // Other handler functions remain the same
  const handleSelectWorkflow = async (wf) => {
    setSelectedWorkflow(wf);

    try {
      const detailRes = await getWorkflowDetail(wf.id);
      const wfDetail = detailRes.data;

      // Map backend nodes to ReactFlow nodes
      const rfNodes = wfDetail.nodes.map((n) => ({
        id: n.id.toString(),
        type: 'default', // Add default type for basic node
        position: { 
          x: n.position.x, 
          y: n.position.y 
        },
        data: { 
          label: n.node_type_id ? `Node ${n.id}` : 'Empty Node',
          nodeTypeId: n.node_type_id,
          config: n.config
        },
        style: { 
          width: n.size?.width || 200, 
          height: n.size?.height || 100,
          border: '1px solid #777',
          padding: 10,
          borderRadius: 5,
          background: '#fff'
        }
      }));

      // Map backend edges to ReactFlow edges
      const rfEdges = wfDetail.edges.map((e) => ({
        id: e.id.toString(),
        source: e.source.toString(),
        target: e.target.toString(),
        label: e.label || '',
        type: 'default',  // Add default type for basic edge
        animated: false,
        style: { stroke: '#999' }
      }));

      console.log('Setting nodes:', rfNodes);
      console.log('Setting edges:', rfEdges);

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
      x: n.position.x,
      y: n.position.y,
      width: n.style?.width || 200,
      height: n.style?.height || 100,
      config: n.data.config || ''
    }));

    const backendEdges = edges.map((e) => ({
      source_node_id: parseInt(e.source),
      target_node_id: parseInt(e.target),
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

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  // Fixed onDrop function with proper reactFlowInstance usage
  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const droppedData = event.dataTransfer.getData('application/reactflow');
      
      if (!droppedData) return;

      try {
        const nodeType = JSON.parse(droppedData);
        const reactFlowBounds = event.target.getBoundingClientRect();
        const { zoom } = reactFlowInstance.getViewport();
        
        const position = {
          x: (event.clientX - reactFlowBounds.left) / zoom,
          y: (event.clientY - reactFlowBounds.top) / zoom,
        };

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
      } catch (error) {
        console.error('Error adding new node:', error);
      }
    },
    [reactFlowInstance, setNodes]
  );

  // Return the JSX for the workflow content
  return (
    <div style={{ display: 'flex' }}>
      {/* Left sidebar */}
      <div style={{ width: '250px', borderRight: '1px solid #ccc', padding: '10px' }}>
        {/* Workflow creation form */}
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

        {/* Workflow list */}
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

        {/* Selected workflow controls */}
        {selectedWorkflow && (
          <>
            <h3>Selected: {selectedWorkflow.name}</h3>
            <button onClick={handleSaveWorkflow}>Save</button>
            <button onClick={handleRunWorkflow}>Run</button>
          </>
        )}

        {/* Node library panel */}
        <NodeLibraryPanel nodeTypes={nodeTypes} />
      </div>

      {/* ReactFlow canvas */}
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
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}

// Main export component wrapped with ReactFlowProvider
export default function WorkflowPage() {
  return (
    <ReactFlowProvider>
      <WorkflowContent />
    </ReactFlowProvider>
  );
}