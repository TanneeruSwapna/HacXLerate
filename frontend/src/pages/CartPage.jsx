import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import './CartPage.css';

function CartPage() {
    const [cart, setCart] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const token = localStorage.getItem('token');

    const fetchCart = async () => {
        try {
            setLoading(true);
            const res = await axios.get('http://localhost:5000/api/cart', { headers: { Authorization: `Bearer ${token}` } });
            setCart(res.data);
            setError(null);
        } catch (err) {
            console.error('Failed to fetch cart', err);
            setError('Failed to load cart');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchCart();
        const onCartUpdated = () => fetchCart();
        window.addEventListener('cart-updated', onCartUpdated);
        return () => window.removeEventListener('cart-updated', onCartUpdated);
    }, []);

    const handleQuantityChange = async (productId, newQty) => {
        try {
            await axios.put('http://localhost:5000/api/cart/update', { productId, quantity: newQty }, { headers: { Authorization: `Bearer ${token}` } });
            fetchCart();
            const total = (await axios.get('http://localhost:5000/api/cart', { headers: { Authorization: `Bearer ${token}` } })).data.items.reduce((s, it) => s + (it.quantity || 0), 0);
            window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: total } }));
        } catch (err) {
            console.error('Failed to update quantity', err);
            alert('Failed to update quantity');
        }
    };

    const handleRemove = async (productId) => {
        try {
            // Prefer DELETE with productId in the URL (some envs strip DELETE bodies)
            try {
                await axios.delete(`http://localhost:5000/api/cart/remove/${productId}`, { headers: { Authorization: `Bearer ${token}` } });
            } catch (err) {
                // Fallback to POST /remove if DELETE with URL fails
                await axios.post('http://localhost:5000/api/cart/remove', { productId }, { headers: { Authorization: `Bearer ${token}` } });
            }
            await fetchCart();
            const total = (await axios.get('http://localhost:5000/api/cart', { headers: { Authorization: `Bearer ${token}` } })).data.items.reduce((s, it) => s + (it.quantity || 0), 0);
            window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: total } }));
        } catch (err) {
            console.error('Failed to remove item', err);
            alert('Failed to remove item');
        }
    };

    if (loading) return <div className="page-container">Loading cart...</div>;
    if (error) return <div className="page-container">{error}</div>;

    const items = cart?.items || [];
    const subtotal = items.reduce((s, it) => s + ((it.productId?.price || 0) * (it.quantity || 0)), 0);
    const shipping = items.length ? 25 : 0;
    const total = subtotal + shipping;

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">Shopping Cart</h1>
                <p className="page-subtitle">Review your items before checkout</p>
            </div>

            {items.length > 0 ? (
                <div className="cart-content">
                    <div className="cart-items">
                        {items.map((item) => {
                            const pid = item.productId && item.productId._id ? String(item.productId._id) : String(item.productId);
                            return (
                                <div key={`${pid}-${item._id || ''}`} className="cart-item">
                                    <div className="item-image">
                                        {item.productId && item.productId.images && item.productId.images[0] ? (
                                            <img src={item.productId.images[0]} alt={item.productId.name} />
                                        ) : (
                                            <span className="placeholder-icon">📦</span>
                                        )}
                                    </div>
                                    <div className="item-details">
                                        <h3 className="item-name">{item.productId?.name}</h3>
                                        <p className="item-category">{item.productId?.category}</p>
                                        <div className="item-price">${(item.productId?.price || 0).toFixed(2)}</div>
                                    </div>
                                    <div className="item-quantity">
                                        <label>Quantity</label>
                                        <input type="number" value={item.quantity} min="1" className="quantity-input" onChange={(e) => handleQuantityChange(pid, Number(e.target.value))} />
                                    </div>
                                    <div className="item-total">${((item.productId?.price || 0) * item.quantity).toFixed(2)}</div>
                                    <div className="item-actions">
                                        <button className="btn btn-danger" onClick={() => handleRemove(pid)}>Remove</button>
                                    </div>
                                </div>
                            );
                        })}
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
                            <button className="btn btn-primary checkout-btn">Proceed to Checkout</button>
                            <Link to="/products" className="continue-shopping">Continue Shopping</Link>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="empty-cart">
                    <div className="empty-cart-icon">🛒</div>
                    <h3>Your cart is empty</h3>
                    <p>Add some products to get started</p>
                    <Link to="/products" className="btn btn-primary">Browse Products</Link>
                </div>
            )}
        </div>
    );
}

export default CartPage;