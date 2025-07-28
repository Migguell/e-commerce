import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useApp } from '../../context/AppContext';
import './Login.css';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  
  const { login } = useApp();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Get the intended destination or default to home
  const from = location.state?.from?.pathname || '/';

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Basic validation
      if (!formData.email || !formData.password) {
        throw new Error('Please fill in all fields');
      }

      if (!isValidEmail(formData.email)) {
        throw new Error('Please enter a valid email address');
      }

      // In a real app, this would make an API call
      // For demo purposes, we'll simulate a login
      await simulateLogin(formData);
      
      // Mock successful login
      const userData = {
        id: 1,
        name: 'John Doe',
        email: formData.email,
        avatar: '/api/placeholder/100/100'
      };
      
      const token = 'mock-jwt-token-' + Date.now();
      
      await login(userData, token);
      
      // Redirect to intended page or home
      navigate(from, { replace: true });
      
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const simulateLogin = (credentials) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulate different login scenarios
        if (credentials.email === 'demo@example.com' && credentials.password === 'password') {
          resolve();
        } else if (credentials.email === 'admin@example.com' && credentials.password === 'admin') {
          resolve();
        } else {
          // For demo, accept any email with password 'password'
          if (credentials.password === 'password') {
            resolve();
          } else {
            reject(new Error('Invalid email or password'));
          }
        }
      }, 1000); // Simulate network delay
    });
  };

  const isValidEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleDemoLogin = () => {
    setFormData({
      email: 'demo@example.com',
      password: 'password'
    });
  };

  return (
    <div className="login-container">
      <div className="container">
        <div className="login-card">
          <div className="login-header">
            <h1>Welcome Back</h1>
            <p>Sign in to your account to continue shopping</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {error && (
              <div className="error-message">
                <span className="error-icon">⚠️</span>
                {error}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email"
                required
                autoComplete="email"
                className={error && !formData.email ? 'error' : ''}
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="password-input">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  required
                  autoComplete="current-password"
                  className={error && !formData.password ? 'error' : ''}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" />
                <span className="checkmark"></span>
                Remember me
              </label>
              <Link to="/forgot-password" className="forgot-link">
                Forgot password?
              </Link>
            </div>

            <button
              type="submit"
              className="btn btn-primary login-btn"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Signing in...
                </>
              ) : (
                'Sign In'
              )}
            </button>

            <div className="demo-section">
              <p>For demo purposes, try:</p>
              <button
                type="button"
                className="btn btn-secondary demo-btn"
                onClick={handleDemoLogin}
              >
                Use Demo Account
              </button>
              <small>Email: demo@example.com, Password: password</small>
            </div>
          </form>

          <div className="login-footer">
            <p>
              Don't have an account?{' '}
              <Link to="/register" className="register-link">
                Sign up here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;