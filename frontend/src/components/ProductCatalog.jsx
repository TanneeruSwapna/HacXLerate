import { useState, useEffect } from 'react';
import axios from 'axios';
import './ProductCatalog.css';

function ProductCatalog() {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: '',
    priceRange: { min: 0, max: 10000 },
    brand: '',
    search: ''
  });
  const [sortBy, setSortBy] = useState('name');
  const [viewMode, setViewMode] = useState('grid');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:5000/api/products', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setProducts(res.data);
        setFilteredProducts(res.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  useEffect(() => {
    let filtered = products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(filters.search.toLowerCase()) ||
        product.description?.toLowerCase().includes(filters.search.toLowerCase());
      const matchesCategory = !filters.category || product.category === filters.category;
      const matchesBrand = !filters.brand || product.brand === filters.brand;
      const matchesPrice = product.price >= filters.priceRange.min && product.price <= filters.priceRange.max;

      return matchesSearch && matchesCategory && matchesBrand && matchesPrice;
    });

    // Sort products
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'price-low':
          return a.price - b.price;
        case 'price-high':
          return b.price - a.price;
        case 'name':
          return a.name.localeCompare(b.name);
        default:
          return 0;
      }
    });

    setFilteredProducts(filtered);
  }, [products, filters, sortBy]);

  const handleAddToCart = async (productId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post('http://localhost:5000/api/cart/add',
        { productId, quantity: 1 },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('Product added to cart!');
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  const categories = [...new Set(products.map(p => p.category))];
  const brands = [...new Set(products.map(p => p.brand).filter(Boolean))];

  if (loading) return <div className="loading">Loading products...</div>;

  return (
    <div className="catalog-container">
      <div className="catalog-header">
        <h1>Product Catalog</h1>
        <div className="catalog-controls">
          <div className="search-section">
            <input
              type="text"
              placeholder="Search products..."
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              className="search-input"
            />
          </div>

          <div className="filter-section">
            <select
              value={filters.category}
              onChange={(e) => setFilters({ ...filters, category: e.target.value })}
              className="filter-select"
            >
              <option value="">All Categories</option>
              {categories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            <select
              value={filters.brand}
              onChange={(e) => setFilters({ ...filters, brand: e.target.value })}
              className="filter-select"
            >
              <option value="">All Brands</option>
              {brands.map(brand => (
                <option key={brand} value={brand}>{brand}</option>
              ))}
            </select>

            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="filter-select"
            >
              <option value="name">Sort by Name</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
            </select>
          </div>

          <div className="view-controls">
            <button
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
            >
              Grid
            </button>
            <button
              className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
            >
              List
            </button>
          </div>
        </div>
      </div>

      <div className="price-filter">
        <label>Price Range: ${filters.priceRange.min} - ${filters.priceRange.max}</label>
        <input
          type="range"
          min="0"
          max="10000"
          value={filters.priceRange.max}
          onChange={(e) => setFilters({
            ...filters,
            priceRange: { ...filters.priceRange, max: parseInt(e.target.value) }
          })}
        />
      </div>

      <div className={`products-${viewMode}`}>
        {filteredProducts.map((product) => (
          <div key={product._id} className={`product-card ${viewMode}`}>
            {product.images && product.images.length > 0 && (
              <div className="product-image">
                <img src={product.images[0]} alt={product.name} />
              </div>
            )}

            <div className="product-info">
              <div className="product-header">
                <h3 className="product-name">{product.name}</h3>
                <div className="product-brand">{product.brand}</div>
              </div>

              <div className="product-description">
                {product.description}
              </div>

              <div className="product-specs">
                {product.specifications && (
                  <div className="specs">
                    {product.specifications.weight && <span>Weight: {product.specifications.weight}</span>}
                    {product.specifications.dimensions && <span>Dimensions: {product.specifications.dimensions}</span>}
                    {product.specifications.material && <span>Material: {product.specifications.material}</span>}
                  </div>
                )}
              </div>

              <div className="product-pricing">
                <div className="price-section">
                  <div className="main-price">${product.price}</div>
                  {product.pricing?.wholesale && (
                    <div className="wholesale-price">Wholesale: ${product.pricing.wholesale}</div>
                  )}
                </div>

                {product.inventory && (
                  <div className="inventory-info">
                    <div className="stock">Stock: {product.inventory.quantity}</div>
                    <div className="min-order">Min Order: {product.inventory.minOrderQuantity}</div>
                  </div>
                )}
              </div>

              <div className="product-actions">
                <button
                  className="add-to-cart-btn"
                  onClick={() => handleAddToCart(product._id)}
                  disabled={!product.inventory?.quantity}
                >
                  Add to Cart
                </button>
                <button className="wishlist-btn">♡</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredProducts.length === 0 && (
        <div className="no-products">
          <h3>No products found</h3>
          <p>Try adjusting your filters</p>
        </div>
      )}
    </div>
  );
}

export default ProductCatalog;