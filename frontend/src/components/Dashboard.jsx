import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


function Dashboard() {
  const [stats, setStats] = useState({
    totalOrders: 0,
    totalSpent: 0,
    pendingOrders: 0,
    recommendations: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('token');
        const [statsRes, recsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/dashboard/stats`, {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get(`${API_BASE_URL}/recommendations`, {
            headers: { Authorization: `Bearer ${token}` }
          })
        ]);
        setStats({
          ...statsRes.data,
          recommendations: recsRes.data.slice(0, 3)
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome to Qwipo!</h1>
        <p>Your personalized B2B marketplace dashboard</p>
      </div>

      <div className="dashboard-grid">
        <div className="stats-section">
          <h2>Business Overview</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">📦</div>
              <div className="stat-content">
                <div className="stat-value">{stats.totalOrders}</div>
                <div className="stat-label">Total Orders</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">💰</div>
              <div className="stat-content">
                <div className="stat-value">${stats.totalSpent.toLocaleString()}</div>
                <div className="stat-label">Total Spent</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⏳</div>
              <div className="stat-content">
                <div className="stat-value">{stats.pendingOrders}</div>
                <div className="stat-label">Pending Orders</div>
              </div>
            </div>
          </div>
        </div>

        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-buttons">
            <Link to="/catalog" className="action-btn primary">
              <div className="btn-icon">🛍️</div>
              <div className="btn-content">
                <div className="btn-title">Browse Catalog</div>
                <div className="btn-subtitle">Discover new products</div>
              </div>
            </Link>

            <Link to="/recommendations" className="action-btn secondary">
              <div className="btn-icon">🎯</div>
              <div className="btn-content">
                <div className="btn-title">Get Recommendations</div>
                <div className="btn-subtitle">AI-powered suggestions</div>
              </div>
            </Link>

            <Link to="/cart" className="action-btn tertiary">
              <div className="btn-icon">🛒</div>
              <div className="btn-content">
                <div className="btn-title">View Cart</div>
                <div className="btn-subtitle">Review your items</div>
              </div>
            </Link>

            <Link to="/analytics" className="action-btn quaternary">
              <div className="btn-icon">📊</div>
              <div className="btn-content">
                <div className="btn-title">Analytics</div>
                <div className="btn-subtitle">Business insights</div>
              </div>
            </Link>
          </div>
        </div>

        <div className="recommendations-preview">
          <h2>Recommended for You</h2>
          <div className="recommendation-cards">
            {stats.recommendations.map((rec, index) => (
              <div key={index} className="recommendation-card">
                <div className="rec-product">{rec.product}</div>
                <div className="rec-score">Score: {(rec.score * 100).toFixed(1)}%</div>
                <div className="rec-reason">{rec.reason}</div>
              </div>
            ))}
          </div>
          <Link to="/recommendations" className="view-all-btn">View All Recommendations</Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;