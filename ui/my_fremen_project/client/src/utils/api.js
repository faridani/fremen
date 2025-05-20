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
