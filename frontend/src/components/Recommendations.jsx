import { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import './Recommendations.css';

const socket = io('http://localhost:5000');

function Recommendations() {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('score');

  useEffect(() => {
    const fetchRecs = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:5000/api/recommendations', {
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
              <button className="add-to-cart-btn">Add to Cart</button>
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