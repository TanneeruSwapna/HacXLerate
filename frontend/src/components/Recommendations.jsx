import { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import './Recommendations.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


const socket = io(API_BASE_URL);

function Recommendations() {
  const [recs, setRecs] = useState([]);
  const [adding, setAdding] = useState({});
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('score');

  useEffect(() => {
    const fetchRecs = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(`${API_BASE_URL}/recommendations`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setRecs(res.data);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchRecs();

    socket.on('new-recommendation', (rec) => {
      setRecs((prev) => [...prev, rec]);
    });

    return () => socket.off('new-recommendation');
  }, []);

  const filteredRecs = recs.filter(rec => {
    if (filterType === 'all') return true;
    if (filterType === 'high-score') return rec.score > 0.7;
    if (filterType === 'medium-score') return rec.score > 0.4 && rec.score <= 0.7;
    if (filterType === 'low-score') return rec.score <= 0.4;
    return true;
  });

  const sortedRecs = [...filteredRecs].sort((a, b) => {
    switch (sortBy) {
      case 'score':
        return b.score - a.score;
      case 'similarity':
        return b.sim - a.sim;
      case 'name':
        return a.product.localeCompare(b.product);
      default:
        return 0;
    }
  });

  const getScoreColor = (score) => {
    if (score > 0.7) return 'high-score';
    if (score > 0.4) return 'medium-score';
    return 'low-score';
  };

  const getScoreLabel = (score) => {
    if (score > 0.7) return 'Highly Recommended';
    if (score > 0.4) return 'Recommended';
    return 'Consider';
  };

  const resolveProductId = async (rec) => {
    // Try common id fields first
    if (rec.productId) return rec.productId;
    if (rec.id) return rec.id;
    if (rec._id) return rec._id;

    // Fallback: try to lookup product by name
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get(`${API_BASE_URL}/products?search=` + encodeURIComponent(rec.product), {
        headers: { Authorization: `Bearer ${token}` }
      });
      const list = res.data || [];
      if (list.length > 0) return list[0]._id || list[0].id;
    } catch (err) {
      console.warn('Failed to resolve product id for recommendation', err);
    }
    return null;
  };

  const handleAddToCart = async (rec, idx) => {
    const key = String(idx);
    setAdding((s) => ({ ...s, [key]: true }));
    try {
      const productId = await resolveProductId(rec);
      if (!productId) {
        alert('Cannot find product id for this recommendation');
        return;
      }

      const token = localStorage.getItem('token');
      await axios.post(`${API_BASE_URL}/cart/add`, { productId, quantity: 1 }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      // Refresh cart count for navbar
      const cartRes = await axios.get(`${API_BASE_URL}/cart`, { headers: { Authorization: `Bearer ${token}` } });
      const total = (cartRes.data.items || []).reduce((s, it) => s + (it.quantity || 0), 0);
      window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: total } }));
      alert('Added to cart');
    } catch (err) {
      console.error('Failed to add recommendation to cart', err);
      alert('Failed to add to cart');
    } finally {
      setAdding((s) => ({ ...s, [key]: false }));
    }
  };

  if (loading) return <div className="loading">Loading recommendations...</div>;

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h1>AI-Powered Recommendations</h1>
        <p>Personalized product suggestions based on your business profile and purchase history</p>

        <div className="recommendations-controls">
          <div className="filter-controls">
            <label>Filter by Score:</label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Recommendations</option>
              <option value="high-score">High Score (70%+)</option>
              <option value="medium-score">Medium Score (40-70%)</option>
              <option value="low-score">Low Score (40%-)</option>
            </select>
          </div>

          <div className="sort-controls">
            <label>Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-select"
            >
              <option value="score">Recommendation Score</option>
              <option value="similarity">Similarity Score</option>
              <option value="name">Product Name</option>
            </select>
          </div>
        </div>
      </div>

      <div className="recommendations-grid">
        {sortedRecs.map((rec, index) => (
          <div key={index} className={`recommendation-card ${getScoreColor(rec.score)}`}>
            <div className="rec-header">
              <div className="rec-product">{rec.product}</div>
              <div className="rec-badges">
                <span className={`score-badge ${getScoreColor(rec.score)}`}>
                  {getScoreLabel(rec.score)}
                </span>
                <span className="score-value">{(rec.score * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div className="rec-metrics">
              <div className="metric">
                <span className="metric-label">AI Score:</span>
                <span className="metric-value">{(rec.score * 100).toFixed(1)}%</span>
              </div>
              <div className="metric">
                <span className="metric-label">Similarity:</span>
                <span className="metric-value">{(rec.sim * 100).toFixed(1)}%</span>
              </div>
            </div>

            <div className="rec-reason">
              <h4>Why this recommendation?</h4>
              <p>{rec.reason}</p>
            </div>

            <div className="rec-actions">
              <button className="view-product-btn">View Product</button>
              <button className="add-to-cart-btn" onClick={() => handleAddToCart(rec, index)} disabled={!!adding[String(index)]}>
                {adding[String(index)] ? 'Adding...' : 'Add to Cart'}
              </button>
              <button className="save-btn">Save for Later</button>
            </div>
          </div>
        ))}
      </div>

      {sortedRecs.length === 0 && (
        <div className="no-recommendations">
          <h3>No recommendations found</h3>
          <p>Try adjusting your filters or complete your business profile for better suggestions.</p>
        </div>
      )}

      <div className="recommendations-footer">
        <div className="insights">
          <h3>Recommendation Insights</h3>
          <div className="insight-stats">
            <div className="insight-item">
              <span className="insight-label">Total Recommendations:</span>
              <span className="insight-value">{recs.length}</span>
            </div>
            <div className="insight-item">
              <span className="insight-label">High Confidence:</span>
              <span className="insight-value">{recs.filter(r => r.score > 0.7).length}</span>
            </div>
            <div className="insight-item">
              <span className="insight-label">Last Updated:</span>
              <span className="insight-value">Just now</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Recommendations;