import { Routes, Route, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import AboutPage from './pages/AboutPage';
import DashboardPage from './pages/DashboardPage';
import ProductCatalogPage from './pages/ProductCatalogPage';
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