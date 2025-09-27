import { Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ProductCatalog from './components/ProductCatalog';
import Recommendations from './components/Recommendations';
import Cart from './components/Cart';
import './App.css';

const App = () => (
    <div className="app-container">
      <header>
        <div className="logo">Qwipo</div>
        <div className="search-bar">
          <input type="text" placeholder="Search for Products, Brands and More" />
        </div>
        <div className="nav-links">
          <a href="/dashboard">Dashboard</a>
          <a href="/recommendations">Recommendations</a>
          <div className="cart-icon" data-count="0">Cart</div> {/* Update count dynamically in real app */}
        </div>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/catalog" element={<ProductCatalog />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/cart" element={<Cart />} />
        </Routes>
      </main>
    </div>
  );

export default App;