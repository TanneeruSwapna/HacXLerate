import { Link } from 'react-router-dom';
import './LandingPage.css';

function LandingPage() {
    return (
        <div className="landing-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-container">
                    <div className="hero-content">
                        <div className="hero-badge">
                            <span className="badge-icon">🏢</span>
                            <span>B2B Marketplace</span>
                        </div>
                        <h1 className="hero-title">
                            Connect, Trade, and Grow Your Business
                        </h1>
                        <p className="hero-subtitle">
                            Join thousands of businesses already using our platform to discover new opportunities,
                            manage inventory, and expand their network in the B2B marketplace.
                        </p>
                        <div className="hero-actions">
                            <Link to="/register" className="btn btn-primary btn-large">
                                Get Started Free
                            </Link>
                            <Link to="/about" className="btn btn-outline btn-large">
                                Learn More
                            </Link>
                        </div>
                        <div className="hero-stats">
                            <div className="stat">
                                <div className="stat-number">10,000+</div>
                                <div className="stat-label">Active Businesses</div>
                            </div>
                            <div className="stat">
                                <div className="stat-number">$50M+</div>
                                <div className="stat-label">Total Transactions</div>
                            </div>
                            <div className="stat">
                                <div className="stat-number">150+</div>
                                <div className="stat-label">Countries</div>
                            </div>
                        </div>
                    </div>
                    <div className="hero-image">
                        <div className="hero-visual">
                            <div className="floating-card card-1">
                                <div className="card-icon">📦</div>
                                <div className="card-text">Product Management</div>
                            </div>
                            <div className="floating-card card-2">
                                <div className="card-icon">🤝</div>
                                <div className="card-text">Business Connections</div>
                            </div>
                            <div className="floating-card card-3">
                                <div className="card-icon">📊</div>
                                <div className="card-text">Analytics & Insights</div>
                            </div>
                            <div className="floating-card card-4">
                                <div className="card-icon">🎯</div>
                                <div className="card-text">AI Recommendations</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Everything You Need for B2B Success</h2>
                        <p className="section-subtitle">
                            Powerful tools and features designed specifically for business-to-business commerce
                        </p>
                    </div>
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="feature-icon">📦</div>
                            <h3 className="feature-title">Product Catalog</h3>
                            <p className="feature-description">
                                Manage your product inventory with detailed specifications, pricing tiers, and automated SKU generation.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🎯</div>
                            <h3 className="feature-title">AI Recommendations</h3>
                            <p className="feature-description">
                                Get intelligent product recommendations and market insights powered by advanced machine learning.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">📊</div>
                            <h3 className="feature-title">Analytics Dashboard</h3>
                            <p className="feature-description">
                                Track your business performance with comprehensive analytics and real-time reporting.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🤝</div>
                            <h3 className="feature-title">Business Network</h3>
                            <p className="feature-description">
                                Connect with suppliers, distributors, and partners in a trusted B2B ecosystem.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">🔒</div>
                            <h3 className="feature-title">Secure Transactions</h3>
                            <p className="feature-description">
                                Enterprise-grade security and compliance for all your business transactions.
                            </p>
                        </div>
                        <div className="feature-card">
                            <div className="feature-icon">📱</div>
                            <h3 className="feature-title">Mobile Ready</h3>
                            <p className="feature-description">
                                Access your business dashboard and manage operations from anywhere, anytime.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">How It Works</h2>
                        <p className="section-subtitle">
                            Get started in three simple steps
                        </p>
                    </div>
                    <div className="steps-container">
                        <div className="step">
                            <div className="step-number">1</div>
                            <div className="step-content">
                                <h3 className="step-title">Create Your Account</h3>
                                <p className="step-description">
                                    Sign up with your business information and verify your company details.
                                </p>
                            </div>
                        </div>
                        <div className="step">
                            <div className="step-number">2</div>
                            <div className="step-content">
                                <h3 className="step-title">Add Your Products</h3>
                                <p className="step-description">
                                    Upload your product catalog with detailed specifications and pricing.
                                </p>
                            </div>
                        </div>
                        <div className="step">
                            <div className="step-number">3</div>
                            <div className="step-content">
                                <h3 className="step-title">Start Trading</h3>
                                <p className="step-description">
                                    Connect with other businesses, receive orders, and grow your network.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="cta-section">
                <div className="container">
                    <div className="cta-content">
                        <h2 className="cta-title">Ready to Transform Your B2B Business?</h2>
                        <p className="cta-subtitle">
                            Join thousands of businesses already growing with our platform
                        </p>
                        <div className="cta-actions">
                            <Link to="/register" className="btn btn-primary btn-large">
                                Start Free Trial
                            </Link>
                            <Link to="/login" className="btn btn-outline btn-large">
                                Sign In
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            {/* Footer */}
            
        </div>
    );
}

export default LandingPage;
