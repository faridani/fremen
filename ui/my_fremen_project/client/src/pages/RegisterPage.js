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
