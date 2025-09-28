import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ProductDetailPage.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


export default function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [editing, setEditing] = useState(false);
    const [form, setForm] = useState({});

    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const res = await axios.get(`${API_BASE_URL}/products/${id}`);
                setProduct(res.data);
                setForm({
                    name: res.data.name || '',
                    description: res.data.description || '',
                    price: res.data.price || 0,
                    category: res.data.category || '',
                    'inventory.quantity': res.data.inventory?.quantity ?? 0
                });
            } catch (err) {
                setError('Could not load product');
            } finally {
                setLoading(false);
            }
        };
        fetchProduct();
    }, [id]);

    const isOwner = () => {
        if (!user || !product) return false;
        return user._id === String(product.createdBy?._id || product.createdBy);
    };

    const handleEditToggle = () => {
        setEditing((s) => !s);
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((f) => ({ ...f, [name]: value }));
    };

    const handleSave = async () => {
        try {
            const payload = {
                name: form.name,
                description: form.description,
                price: Number(form.price),
                category: form.category,
                inventory: { quantity: Number(form['inventory.quantity'] || 0) }
            };

            const res = await axios.put(`http://localhost:5000/api/products/${id}`, payload, { headers: { Authorization: `Bearer ${token}` } });
            setProduct(res.data);
            setEditing(false);
            alert('Product updated');
        } catch (err) {
            console.error(err);
            alert('Failed to update product');
        }
    };

    if (loading) return <div className="page-container">Loading product...</div>;
    if (error) return <div className="page-container">{error}</div>;
    if (!product) return <div className="page-container">Product not found</div>;

    return (
        <div className="page-container product-detail">
            <Link to="/products" className="back-link">← Back to catalog</Link>
            <div className="detail-grid">
                <div className="detail-images">
                    {product.images && product.images.length ? (
                        <img src={product.images[0]} alt={product.name} />
                    ) : (
                        <div className="placeholder-icon">No image</div>
                    )}
                </div>
                <div className="detail-info">
                    {!editing ? (
                        <>
                            <h1 className="detail-name">{product.name}</h1>
                            <div className="detail-meta">
                                <span className="detail-category">{product.category}</span>
                                <span className="detail-price">${product.price}</span>
                            </div>
                            <p className="detail-description">{product.description}</p>
                            <div className="detail-extra">
                                <p><strong>SKU:</strong> {product.sku}</p>
                                <p><strong>Stock:</strong> {product.inventory?.quantity ?? 'N/A'}</p>
                                <p><strong>Created by:</strong> {product.createdBy?.name ?? 'Unknown'}</p>
                            </div>
                            {isOwner() && <button className="btn btn-secondary" onClick={handleEditToggle}>Edit Product</button>}
                        </>
                    ) : (
                        <div className="edit-form">
                            <div className="form-group">
                                <label>Name</label>
                                <input name="name" value={form.name} onChange={handleChange} />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea name="description" value={form.description} onChange={handleChange} />
                            </div>
                            <div className="form-group">
                                <label>Price</label>
                                <input name="price" type="number" value={form.price} onChange={handleChange} />
                            </div>
                            <div className="form-group">
                                <label>Category</label>
                                <input name="category" value={form.category} onChange={handleChange} />
                            </div>
                            <div className="form-group">
                                <label>Stock</label>
                                <input name="inventory.quantity" type="number" value={form['inventory.quantity']} onChange={handleChange} />
                            </div>
                            <div className="form-actions">
                                <button className="btn btn-primary" onClick={handleSave}>Save</button>
                                <button className="btn" onClick={handleEditToggle}>Cancel</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
