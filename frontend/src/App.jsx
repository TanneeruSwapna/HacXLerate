import { Routes, Route, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProductCatalogPage from './pages/ProductCatalogPage';
import RecommendationsPage from './pages/RecommendationsPage';
import CartPage from './pages/CartPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ProfilePage from './pages/ProfilePage';
import './App.css';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [cartCount, setCartCount] = useState(0);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    setIsMobileMenuOpen(false);
  };

  return (
    <div className="app-container">
      {/* Enhanced Navbar */}
      {isAuthenticated && (
        <header className="main-header">
          <div className="header-content">
            {/* Logo Section */}
            <div className="logo-section">
              <Link to="/dashboard" className="logo-link">
                <div className="logo">Qwipo</div>
                <span className="tagline">B2B Marketplace</span>
              </Link>
            </div>

            {/* Search Section */}
            <div className="search-section">
              <div className="search-bar">
                <input
                  type="text"
                  placeholder="Search products, brands, categories..."
                  className="search-input"
                />
                <button className="search-btn">🔍</button>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="nav-section desktop-nav">
              <Link to="/dashboard" className="nav-link">
                <span className="nav-icon">📊</span>
                Dashboard
              </Link>
              <Link to="/catalog" className="nav-link">
                <span className="nav-icon">📦</span>
                Catalog
              </Link>
              <Link to="/recommendations" className="nav-link">
                <span className="nav-icon">🎯</span>
                Recommendations
              </Link>
              <Link to="/analytics" className="nav-link">
                <span className="nav-icon">📈</span>
                Analytics
              </Link>
            </nav>

            {/* Right Section - Cart and User */}
            <div className="right-section">
              <Link to="/cart" className="cart-link">
                <span className="cart-icon">🛒</span>
                <span className="cart-text">Cart</span>
                <span className="cart-count">{cartCount}</span>
              </Link>

              <div className="user-section">
                <Link to="/profile" className="user-link">
                  <span className="user-icon">👤</span>
                  <span className="user-name">{user?.businessInfo?.companyName || 'Profile'}</span>
                </Link>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </div>

              {/* Mobile Menu Button */}
              <button 
                className="mobile-menu-btn"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                ☰
              </button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {isMobileMenuOpen && (
            <div className="mobile-nav">
              <Link to="/dashboard" className="mobile-nav-link" onClick={() => setIsMobileMenuOpen(false)}>
                <span className="nav-icon">📊</span>
                Dashboard
              </Link>
              <Link to="/catalog" className="mobile-nav-link" onClick={() => setIsMobileMenuOpen(false)}>
                <span className="nav-icon">📦</span>
                Catalog
              </Link>
              <Link to="/recommendations" className="mobile-nav-link" onClick={() => setIsMobileMenuOpen(false)}>
                <span className="nav-icon">🎯</span>
                Recommendations
              </Link>
              <Link to="/analytics" className="mobile-nav-link" onClick={() => setIsMobileMenuOpen(false)}>
                <span className="nav-icon">📈</span>
                Analytics
              </Link>
              <Link to="/profile" className="mobile-nav-link" onClick={() => setIsMobileMenuOpen(false)}>
                <span className="nav-icon">👤</span>
                Profile
              </Link>
              <button onClick={handleLogout} className="mobile-logout-btn">
                Logout
              </button>
            </div>
          )}
        </header>
      )}

      {/* Main Content */}
      <main className={isAuthenticated ? 'authenticated-main' : 'main'}>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/catalog" element={<ProductCatalogPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="main-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Qwipo</h3>
            <p>Your trusted B2B marketplace for business growth and success.</p>
            <div className="social-links">
              <a href="#" className="social-link">📘</a>
              <a href="#" className="social-link">🐦</a>
              <a href="#" className="social-link">💼</a>
              <a href="#" className="social-link">📧</a>
            </div>
          </div>
          
          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><Link to="/dashboard">Dashboard</Link></li>
              <li><Link to="/catalog">Product Catalog</Link></li>
              <li><Link to="/recommendations">Recommendations</Link></li>
              <li><Link to="/analytics">Analytics</Link></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Support</h4>
            <ul>
              <li><a href="#">Help Center</a></li>
              <li><a href="#">Contact Us</a></li>
              <li><a href="#">API Documentation</a></li>
              <li><a href="#">Status Page</a></li>
            </ul>
          </div>
          
          <div className="footer-section">
            <h4>Company</h4>
            <ul>
              <li><a href="#">About Us</a></li>
              <li><a href="#">Careers</a></li>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2024 Qwipo B2B Marketplace. All rights reserved.</p>
          <p>Built with ❤️ for business success</p>
        </div>
      </footer>
    </div>
  );
};

export default App;