import { useState, useEffect } from 'react';
import axios from 'axios';
import './Cart.css';

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get('http://localhost:5000/api/cart', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setCartItems(res.data.items || []);
      } catch (error) {
        console.error('Error fetching cart:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchCart();
  }, []);

  const updateQuantity = async (productId, newQuantity) => {
    if (newQuantity < 1) return;

    setUpdating(true);
    try {
      const token = localStorage.getItem('token');
      await axios.put('http://localhost:5000/api/cart/update',
        { productId, quantity: newQuantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setCartItems(prev =>
        prev.map(item =>
          item.productId._id === productId
            ? { ...item, quantity: newQuantity }
            : item
        )
      );
    } catch (error) {
      console.error('Error updating quantity:', error);
    } finally {
      setUpdating(false);
    }
  };

  const removeItem = async (productId) => {
    setUpdating(true);
    try {
      const token = localStorage.getItem('token');
      await axios.delete('http://localhost:5000/api/cart/remove', {
        data: { productId },
        headers: { Authorization: `Bearer ${token}` }
      });

      setCartItems(prev => prev.filter(item => item.productId._id !== productId));
    } catch (error) {
      console.error('Error removing item:', error);
    } finally {
      setUpdating(false);
    }
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => {
      return total + (item.productId.price * item.quantity);
    }, 0);
  };

  const calculateSavings = () => {
    // Mock bulk discount calculation
    return cartItems.reduce((savings, item) => {
      if (item.quantity >= 10) {
        return savings + (item.productId.price * item.quantity * 0.1);
      }
      return savings;
    }, 0);
  };

  if (loading) return <div className="loading">Loading cart...</div>;

  return (
    <div className="cart-container">
      <div className="cart-header">
        <h1>Shopping Cart</h1>
        <div className="cart-summary">
          <span className="item-count">{cartItems.length} items</span>
        </div>
      </div>

      {cartItems.length === 0 ? (
        <div className="empty-cart">
          <h3>Your cart is empty</h3>
          <p>Add some products to get started</p>
          <a href="/catalog" className="browse-btn">Browse Products</a>
        </div>
      ) : (
        <div className="cart-content">
          <div className="cart-items">
            {cartItems.map((item) => (
              <div key={item.productId._id} className="cart-item">
                <div className="item-image">
                  {item.productId.images && item.productId.images.length > 0 ? (
                    <img src={item.productId.images[0]} alt={item.productId.name} />
                  ) : (
                    <div className="placeholder-image">📦</div>
                  )}
                </div>

                <div className="item-details">
                  <h3 className="item-name">{item.productId.name}</h3>
                  <p className="item-brand">{item.productId.brand}</p>
                  <p className="item-category">{item.productId.category}</p>

                  {item.productId.specifications && (
                    <div className="item-specs">
                      {item.productId.specifications.weight && (
                        <span>Weight: {item.productId.specifications.weight}</span>
                      )}
                      {item.productId.specifications.material && (
                        <span>Material: {item.productId.specifications.material}</span>
                      )}
                    </div>
                  )}
                </div>

                <div className="item-pricing">
                  <div className="price-per-unit">
                    ${item.productId.price} each
                  </div>
                  {item.productId.pricing?.wholesale && (
                    <div className="wholesale-price">
                      Wholesale: ${item.productId.pricing.wholesale}
                    </div>
                  )}
                </div>

                <div className="item-quantity">
                  <label>Quantity:</label>
                  <div className="quantity-controls">
                    <button
                      onClick={() => updateQuantity(item.productId._id, item.quantity - 1)}
                      disabled={updating || item.quantity <= 1}
                      className="quantity-btn"
                    >
                      -
                    </button>
                    <span className="quantity-value">{item.quantity}</span>
                    <button
                      onClick={() => updateQuantity(item.productId._id, item.quantity + 1)}
                      disabled={updating}
                      className="quantity-btn"
                    >
                      +
                    </button>
                  </div>
                </div>

                <div className="item-total">
                  <div className="line-total">
                    ${(item.productId.price * item.quantity).toFixed(2)}
                  </div>
                  {item.quantity >= 10 && (
                    <div className="bulk-discount">
                      Bulk discount applied!
                    </div>
                  )}
                </div>

                <div className="item-actions">
                  <button
                    onClick={() => removeItem(item.productId._id)}
                    className="remove-btn"
                    disabled={updating}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="cart-summary-section">
            <div className="order-summary">
              <h3>Order Summary</h3>

              <div className="summary-line">
                <span>Subtotal:</span>
                <span>${calculateTotal().toFixed(2)}</span>
              </div>

              {calculateSavings() > 0 && (
                <div className="summary-line savings">
                  <span>Bulk Discount:</span>
                  <span>-${calculateSavings().toFixed(2)}</span>
                </div>
              )}

              <div className="summary-line">
                <span>Shipping:</span>
                <span>Free (B2B)</span>
              </div>

              <div className="summary-line total">
                <span>Total:</span>
                <span>${(calculateTotal() - calculateSavings()).toFixed(2)}</span>
              </div>

              {calculateSavings() > 0 && (
                <div className="savings-message">
                  You saved ${calculateSavings().toFixed(2)} with bulk pricing!
                </div>
              )}
            </div>

            <div className="checkout-actions">
              <button className="checkout-btn primary">
                Proceed to Checkout
              </button>
              <button className="checkout-btn secondary">
                Save for Later
              </button>
              <a href="/catalog" className="continue-shopping">
                Continue Shopping
              </a>
            </div>

            <div className="business-info">
              <h4>Business Benefits</h4>
              <ul>
                <li>✅ Net 30 payment terms available</li>
                <li>✅ Bulk pricing discounts</li>
                <li>✅ Priority shipping</li>
                <li>✅ Dedicated account manager</li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Cart;