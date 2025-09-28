import { Link } from 'react-router-dom';
import './CartPage.css';

function CartPage() {
    // Mock cart data - in real app, this would come from state/API
    const cartItems = [
        {
            id: 1,
            name: 'Office Chair Pro',
            price: 299.99,
            quantity: 1,
            image: null,
            category: 'Furniture'
        },
        {
            id: 2,
            name: 'Wireless Mouse',
            price: 49.99,
            quantity: 2,
            image: null,
            category: 'Electronics'
        }
    ];

    const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const shipping = 25.00;
    const total = subtotal + shipping;

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">Shopping Cart</h1>
                <p className="page-subtitle">Review your items before checkout</p>
            </div>

            {cartItems.length > 0 ? (
                <div className="cart-content">
                    <div className="cart-items">
                        {cartItems.map((item) => (
                            <div key={item.id} className="cart-item">
                                <div className="item-image">
                                    <span className="placeholder-icon">📦</span>
                                </div>
                                <div className="item-details">
                                    <h3 className="item-name">{item.name}</h3>
                                    <p className="item-category">{item.category}</p>
                                    <div className="item-price">${item.price.toFixed(2)}</div>
                                </div>
                                <div className="item-quantity">
                                    <label>Quantity</label>
                                    <input type="number" value={item.quantity} min="1" className="quantity-input" />
                                </div>
                                <div className="item-total">
                                    ${(item.price * item.quantity).toFixed(2)}
                                </div>
                                <div className="item-actions">
                                    <button className="btn btn-danger">Remove</button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="cart-summary">
                        <div className="summary-card">
                            <h3>Order Summary</h3>
                            <div className="summary-line">
                                <span>Subtotal</span>
                                <span>${subtotal.toFixed(2)}</span>
                            </div>
                            <div className="summary-line">
                                <span>Shipping</span>
                                <span>${shipping.toFixed(2)}</span>
                            </div>
                            <div className="summary-line total">
                                <span>Total</span>
                                <span>${total.toFixed(2)}</span>
                            </div>
                            <button className="btn btn-primary checkout-btn">
                                Proceed to Checkout
                            </button>
                            <Link to="/products" className="continue-shopping">
                                Continue Shopping
                            </Link>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="empty-cart">
                    <div className="empty-cart-icon">🛒</div>
                    <h3>Your cart is empty</h3>
                    <p>Add some products to get started</p>
                    <Link to="/products" className="btn btn-primary">
                        Browse Products
                    </Link>
                </div>
            )}
        </div>
    );
}

export default CartPage;