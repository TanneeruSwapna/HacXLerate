import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const res = await axios.post('http://localhost:5000/api/auth/login', { email, password });
      localStorage.setItem('token', res.data.token);
      console.log(res.data.token);
      navigate('/dashboard');
    } catch (err) {
      alert('Login failed! Please check your credentials.');
    }
  };

  return (
    <div className="login-container">
      <div className="login-header">
        <h1>Welcome Back</h1>
        <p>Login to your Qwipo account</p>
        <div className="company-tagline">B2B Marketplace</div>
      </div>

      <div className="form-group">
        <label>Email Address</label>
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button className="login-btn" onClick={handleLogin}>
        Sign In
      </button>

      <div className="register-link">
        <p>New to Qwipo? <Link to="/register">Create an account</Link></p>
      </div>
    </div>
  );
}

export default Login;