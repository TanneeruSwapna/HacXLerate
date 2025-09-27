import { useState, useEffect } from 'react';
import axios from 'axios';

function ProductCatalog() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://localhost:5000/api/products', { headers: { Authorization: `Bearer ${token}` } });
      setProducts(res.data);
    };
    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Product Catalog</h2>
      {products.map((product) => (
        <div key={product._id} className="product-card">
          <h3>{product.name}</h3>
          <p>Price: ${product.price}</p>
          <button>Add to Cart</button> {/* Simulate add */}
        </div>
      ))}
    </div>
  );
}

export default ProductCatalog;