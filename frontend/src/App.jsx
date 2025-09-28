import { Routes, Route, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AboutPage from './pages/AboutPage';
import DashboardPage from './pages/DashboardPage';
import ProductCatalogPage from './pages/ProductCatalogPage';
import ProductDetailPage from './pages/ProductDetailPage';
import AddProductPage from './pages/AddProductPage';
import RecommendationsPage from './pages/RecommendationsPage';
import CartPage from './pages/CartPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ProfilePage from './pages/ProfilePage';
import './App.css';

const App = () => {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [cartCount, setCartCount] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
    // Fetch initial cart count if token present
    const fetchCartCount = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) return;
        const res = await axios.get('http://localhost:5000/api/cart', { headers: { Authorization: `Bearer ${token}` } });
        const items = res.data.items || [];
        const total = items.reduce((s, it) => s + (it.quantity || 0), 0);
        setCartCount(total);
      } catch (err) {
        // ignore
      }
    };
    fetchCartCount();

    // Listen for cart updates from other components
    const onCartUpdated = (e) => {
      if (e && e.detail && typeof e.detail.count === 'number') setCartCount(e.detail.count);
      else fetchCartCount();
    };
    window.addEventListener('cart-updated', onCartUpdated);
    return () => window.removeEventListener('cart-updated', onCartUpdated);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/');
  };

  return (
    <div className="app-container">
      {/* Professional Navbar */}
      <Navbar
        user={user}
        cartCount={cartCount}
        onLogout={handleLogout}
        isAuthenticated={isAuthenticated}
      />

      {/* Main Content */}
      <main className="authenticated-main">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/catalog" element={<ProductCatalogPage />} />
          <Route path="/products" element={<ProductCatalogPage />} />
          <Route path="/products/:id" element={<ProductDetailPage />} />
          <Route path="/add-product" element={<AddProductPage />} />
          <Route path="/recommendations" element={<RecommendationsPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </main>

      {/* Professional Footer */}
      <Footer />
    </div>
  );
};

export default App;