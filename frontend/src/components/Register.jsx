import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Register.css';

function Register() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    companyName: '',
    businessType: 'retailer',
    industry: '',
    businessSize: 'small'
  });
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    if (!formData.email || !formData.password || !formData.companyName) {
      alert('Please fill in all required fields');
      return;
    }

    if (formData.password.length < 6) {
      alert('Password must be at least 6 characters long');
      return;
    }

    try {
      const res = await axios.post('http://localhost:5000/api/auth/register', {
        email: formData.email,
        password: formData.password,
        businessInfo: {
          companyName: formData.companyName,
          businessType: formData.businessType,
          industry: formData.industry,
          businessSize: formData.businessSize
        }
      });
      localStorage.setItem('token', res.data.token);
      navigate('/dashboard');
    } catch (err) {
      alert('Registration failed! Please try again.');
    }
  };

  return (
    <div className="register-container">
      <div className="register-header">
        <h1>Join Qwipo</h1>
        <p>Create your business account</p>
        <div className="company-tagline">B2B Marketplace</div>
      </div>

      <div className="form-group">
        <label>Company Name</label>
        <input
          type="text"
          name="companyName"
          placeholder="Enter your company name"
          value={formData.companyName}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Business Email</label>
        <input
          type="email"
          name="email"
          placeholder="Enter your business email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Password</label>
        <input
          type="password"
          name="password"
          placeholder="Create a strong password"
          value={formData.password}
          onChange={handleInputChange}
          required
        />
      </div>

      <div className="form-group">
        <label>Business Type</label>
        <select
          name="businessType"
          value={formData.businessType}
          onChange={handleInputChange}
        >
          <option value="retailer">Retailer</option>
          <option value="wholesaler">Wholesaler</option>
          <option value="distributor">Distributor</option>
          <option value="manufacturer">Manufacturer</option>
        </select>
      </div>

      <div className="form-group">
        <label>Industry</label>
        <input
          type="text"
          name="industry"
          placeholder="e.g., Technology, Healthcare, Manufacturing"
          value={formData.industry}
          onChange={handleInputChange}
        />
      </div>

      <div className="form-group">
        <label>Business Size</label>
        <select
          name="businessSize"
          value={formData.businessSize}
          onChange={handleInputChange}
        >
          <option value="small">Small (1-50 employees)</option>
          <option value="medium">Medium (51-200 employees)</option>
          <option value="large">Large (201-1000 employees)</option>
          <option value="enterprise">Enterprise (1000+ employees)</option>
        </select>
      </div>

      <button className="register-btn" onClick={handleRegister}>
        Create Account
      </button>

      <div className="login-link">
        <p>Already have an account? <Link to="/">Sign in here</Link></p>
      </div>
    </div>
  );
}

export default Register;