import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar({ user, cartCount, onLogout, isAuthenticated }) {
    const navigate = useNavigate();
    const location = useLocation();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const handleLogout = () => {
        onLogout();
        setIsMobileMenuOpen(false);
        navigate('/');
    };

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    const handleNavClick = () => {
        // Close menu on navigation on mobile
        if (isMobileMenuOpen) {
            setIsMobileMenuOpen(false);
        }
    };

    const isActive = (path) => {
        return location.pathname === path;
    };

    return (
        <nav className="navbar">
            <div className="navbar-container">
                {/* Logo Section */}
                <div className="navbar-logo">
                    <Link to={isAuthenticated ? "/dashboard" : "/"} className="logo-link" onClick={handleNavClick}>
                        <div className="logo">
                            <span className="logo-icon">🏢</span>
                            <span className="logo-text">Qwipo</span>
                        </div>
                    </Link>
                </div>

                {/* Desktop Navigation */}
                <div className="navbar-nav">
                    {isAuthenticated ? (
                        <>
                            {/* Authenticated Links */}
                            <Link
                                to="/dashboard"
                                className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">📊</span>
                                Dashboard
                            </Link>
                            <Link
                                to="/products"
                                className={`nav-link ${isActive('/products') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">📦</span>
                                Products
                            </Link>
                            <Link
                                to="/recommendations"
                                className={`nav-link ${isActive('/recommendations') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">🎯</span>
                                Recommendations
                            </Link>
                        </>
                    ) : (
                        <>
                            {/* Public Links */}
                            <Link
                                to="/"
                                className={`nav-link ${isActive('/') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">🏠</span>
                                Home
                            </Link>
                            <Link
                                to="/about"
                                className={`nav-link ${isActive('/about') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">ℹ️</span>
                                About
                            </Link>
                            <Link
                                to="/products"
                                className={`nav-link ${isActive('/products') ? 'active' : ''}`}
                            >
                                <span className="nav-icon">📦</span>
                                Browse Products
                            </Link>
                        </>
                    )}
                </div>

                {/* Right Section */}
                <div className="navbar-actions">
                    {isAuthenticated ? (
                        <>
                            {/* Cart */}
                            <Link to="/cart" className="cart-link" onClick={handleNavClick}>
                                <span className="cart-icon">🛒</span>
                                <span className="cart-text">Cart</span>
                                {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
                            </Link>

                            {/* Profile */}
                            <Link to="/profile" className="profile-link" onClick={handleNavClick}>
                                <span className="profile-icon">👤</span>
                                <span className="profile-text">Profile</span>
                            </Link>

                            {/* Logout - Essential business action */}
                            <button onClick={handleLogout} className="logout-btn">
                                <span className="logout-icon">🚪</span>
                                <span className="logout-text">Logout</span>
                            </button>
                        </>
                    ) : (
                        <>
                            {/* Login/Register - Replaces Authenticated actions */}
                            <Link to="/login" className="profile-link" onClick={handleNavClick}>
                                <span className="profile-icon">🔑</span>
                                <span className="profile-text">Login</span>
                            </Link>

                            <Link to="/register" className="register-btn"> {/* Class name changed for style differentiation */}
                                <span className="logout-icon">📝</span>
                                <span className="logout-text">Register</span>
                            </Link>
                        </>
                    )}

                    {/* Mobile Menu Toggle */}
                    <button
                        className="mobile-menu-btn"
                        onClick={toggleMobileMenu}
                        aria-expanded={isMobileMenuOpen}
                        aria-controls="mobile-menu"
                    >
                        ☰
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="mobile-menu" id="mobile-menu">
                    {isAuthenticated ? (
                        <>
                            {/* Authenticated Mobile Links */}
                            <Link
                                to="/dashboard"
                                className={`mobile-nav-link ${isActive('/dashboard') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">📊</span> Dashboard
                            </Link>
                            <Link
                                to="/products"
                                className={`mobile-nav-link ${isActive('/products') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">📦</span> Products
                            </Link>
                            <Link
                                to="/recommendations"
                                className={`mobile-nav-link ${isActive('/recommendations') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">🎯</span> Recommendations
                            </Link>
                            <Link
                                to="/cart"
                                className="mobile-nav-link"
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">🛒</span> Cart {cartCount > 0 && `(${cartCount})`}
                            </Link>
                            <Link
                                to="/profile"
                                className="mobile-nav-link"
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">👤</span> Profile
                            </Link>
                            <button onClick={handleLogout} className="mobile-logout-btn">
                                <span className="nav-icon">🚪</span> Logout
                            </button>
                        </>
                    ) : (
                        <>
                            {/* Public Mobile Links */}
                            <Link
                                to="/"
                                className={`mobile-nav-link ${isActive('/') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">🏠</span> Home
                            </Link>
                            <Link
                                to="/about"
                                className={`mobile-nav-link ${isActive('/about') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">ℹ️</span> About
                            </Link>
                            <Link
                                to="/products"
                                className={`mobile-nav-link ${isActive('/products') ? 'active' : ''}`}
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">📦</span> Browse Products
                            </Link>
                            <Link
                                to="/login"
                                className="mobile-nav-link"
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">🔑</span> Login
                            </Link>
                            <Link
                                to="/register"
                                className="mobile-nav-link"
                                onClick={handleNavClick}
                            >
                                <span className="nav-icon">📝</span> Register
                            </Link>
                        </>
                    )}
                </div>
            )}
        </nav>
    );
}

export default Navbar;