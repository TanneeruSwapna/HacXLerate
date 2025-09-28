import './RecommendationsPage.css';

function RecommendationsPage() {
  const recommendations = [
    {
      id: 1,
      product: 'Office Chair Pro',
      reason: 'Based on your recent furniture purchases',
      score: 95,
      price: '$299.99',
      category: 'Furniture'
    },
    {
      id: 2,
      product: 'Wireless Mouse',
      reason: 'Popular among electronics buyers',
      score: 88,
      price: '$49.99',
      category: 'Electronics'
    },
    {
      id: 3,
      product: 'Desk Lamp LED',
      reason: 'Complements your office setup',
      score: 82,
      price: '$79.99',
      category: 'Office Supplies'
    }
  ];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1 className="page-title">AI Recommendations</h1>
        <p className="page-subtitle">Personalized product recommendations for your business</p>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((rec) => (
          <div key={rec.id} className="recommendation-card">
            <div className="recommendation-header">
              <h3 className="product-name">{rec.product}</h3>
              <div className="score-badge">
                <span className="score-value">{rec.score}%</span>
                <span className="score-label">Match</span>
              </div>
            </div>
            <div className="recommendation-body">
              <p className="recommendation-reason">{rec.reason}</p>
              <div className="product-meta">
                <span className="product-price">{rec.price}</span>
                <span className="product-category">{rec.category}</span>
              </div>
            </div>
            <div className="recommendation-actions">
              <button className="btn btn-primary">View Product</button>
              <button className="btn btn-outline">Add to Cart</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationsPage;