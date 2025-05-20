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
