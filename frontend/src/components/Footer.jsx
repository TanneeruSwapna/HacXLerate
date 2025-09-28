import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
    return (
        // <footer className="footer">
    //         <div className="footer-container">
    //             <div className="footer-content">
    //                 {/* Company Info */}
    //                 <div className="footer-section">
    //                     <div className="footer-logo">
    //                         <span className="logo-icon">🏢</span>
    //                         <span className="logo-text">HacXLerate</span>
    //                     </div>
    //                     <p className="footer-description">
    //                         Professional B2B marketplace connecting businesses with quality products and services.
    //                     </p>
    //                 </div>

    //                 {/* Quick Links */}
    //                 <div className="footer-section">
    //                     <h4>Quick Links</h4>
    //                     <ul className="footer-links">
    //                         <li><Link to="/dashboard">Dashboard</Link></li>
    //                         <li><Link to="/products">Products</Link></li>
    //                         <li><Link to="/recommendations">Recommendations</Link></li>
    //                         <li><Link to="/profile">Profile</Link></li>
    //                     </ul>
    //                 </div>

    //                 {/* Support */}
    //                 <div className="footer-section">
    //                     <h4>Support</h4>
    //                     <ul className="footer-links">
    //                         <li><a href="#help">Help Center</a></li>
    //                         <li><a href="#contact">Contact Us</a></li>
    //                         <li><a href="#docs">Documentation</a></li>
    //                         <li><a href="#status">Status</a></li>
    //                     </ul>
    //                 </div>

    //                 {/* Company */}
    //                 <div className="footer-section">
    //                     <h4>Company</h4>
    //                     <ul className="footer-links">
    //                         <li><a href="#about">About Us</a></li>
    //                         <li><a href="#careers">Careers</a></li>
    //                         <li><a href="#privacy">Privacy Policy</a></li>
    //                         <li><a href="#terms">Terms of Service</a></li>
    //                     </ul>
    //                 </div>
    //             </div>

    //             <div className="footer-bottom">
    //                 <p>&copy; 2024 HacXLerate. All rights reserved.</p>
    //             </div>
    //         </div>
    //     </footer>
<footer className="about-footer">
<div className="container">
    <div className="footer-content">
        <div className="footer-brand">
            <span className="logo-icon">🏢</span>
            <span className="logo-text">Qwipo</span>
            <span className="tagline">B2B Marketplace</span>
        </div>
        <div className="footer-links">
            <Link to="/">Home</Link>
            <Link to="/about">About</Link>
            <a href="#">Contact</a>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
        </div>
    </div>
    <div className="footer-bottom">
        <p>&copy; 2024 Qwipo B2B Marketplace. All rights reserved.</p>
    </div>
</div>
</footer>    
);
}

export default Footer;