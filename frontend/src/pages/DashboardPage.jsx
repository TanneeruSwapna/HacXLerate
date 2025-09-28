import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import AddProduct from '../components/AddProduct';
import EditProduct from '../components/EditProduct';
import './DashboardPage.css';

function DashboardPage() {
    const [showAddProduct, setShowAddProduct] = useState(false);
    const [myProducts, setMyProducts] = useState([]);
    const [loading, setLoading] = useState(false);
    const [activeTab, setActiveTab] = useState('dashboard'); // 'dashboard', 'add-product', 'my-products'
    const [editingProduct, setEditingProduct] = useState(null);

    useEffect(() => {
        if (activeTab === 'my-products') {
            fetchMyProducts();
        }
    }, [activeTab]);

    const fetchMyProducts = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem('token');
            const response = await axios.get(`${API_BASE_URL}/products/my-products`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMyProducts(response.data);
        } catch (error) {
            console.error('Error fetching my products:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleProductAdded = () => {
        setActiveTab('my-products');
        fetchMyProducts();
    };

    const handleEditClick = (product) => {
        setEditingProduct(product);
    };

    const handleUpdated = async () => {
        setEditingProduct(null);
        await fetchMyProducts();
    };

    const renderContent = () => {
        switch (activeTab) {
            case 'add-product':
                return (
                    <div className="dashboard-add-product">
                        <div className="flex-between mb-4">
                            <h2>Add New Product</h2>
                            <button
                                className="btn btn-secondary"
                                onClick={() => setActiveTab('dashboard')}
                            >
                                Back to Dashboard
                            </button>
                        </div>
                        <AddProduct onProductAdded={handleProductAdded} />
                    </div>
                );

            case 'my-products':
                return (
                    <div className="dashboard-my-products">
                        <div className="flex-between mb-4">
                            <h2>My Products</h2>
                            <button
                                className="btn btn-primary"
                                onClick={() => setActiveTab('add-product')}
                            >
                                Add New Product
                            </button>
                        </div>

                        {loading ? (
                            <div className="loading">Loading your products...</div>
                        ) : myProducts.length > 0 ? (
                            <div className="my-products-grid">
                                {myProducts.map((product) => (
                                    <div key={product._id} className="product-card">
                                        <div className="product-image">
                                            {product.images && product.images.length > 0 ? (
                                                <img src={product.images[0]} alt={product.name} />
                                            ) : (
                                                <span className="placeholder-icon">📦</span>
                                            )}
                                        </div>
                                        <div className="product-info">
                                            <h3 className="product-name">{product.name}</h3>
                                            <p className="product-description">{product.description}</p>
                                            <div className="product-meta">
                                                <span className="product-category">{product.category}</span>
                                                <span className="product-price">${product.price}</span>
                                            </div>
                                            <div className="product-actions">
                                                <button className="btn btn-secondary" onClick={() => handleEditClick(product)}>Edit</button>
                                                <button className="btn btn-danger">Delete</button>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="empty-products">
                                <div className="placeholder-icon">📦</div>
                                <h3>No products yet</h3>
                                <p>Start by adding your first product</p>
                                <button
                                    className="btn btn-primary"
                                    onClick={() => setActiveTab('add-product')}
                                >
                                    Add Product
                                </button>
                            </div>
                        )}
                    </div>
                );

            default:
                return (
                    <div className="dashboard-content">
                        <div className="dashboard-stats">
                            <div className="stat-card">
                                <div className="stat-icon">📦</div>
                                <div className="stat-info">
                                    <h3>{myProducts.length}</h3>
                                    <p>My Products</p>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon">👥</div>
                                <div className="stat-info">
                                    <h3>0</h3>
                                    <p>Customers</p>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon">💰</div>
                                <div className="stat-info">
                                    <h3>$0</h3>
                                    <p>Revenue</p>
                                </div>
                            </div>
                            <div className="stat-card">
                                <div className="stat-icon">📈</div>
                                <div className="stat-info">
                                    <h3>0%</h3>
                                    <p>Growth</p>
                                </div>
                            </div>
                        </div>

                        <div className="dashboard-actions">
                            <div className="action-card" onClick={() => setActiveTab('add-product')}>
                                <div className="action-icon">➕</div>
                                <h3>Add Product</h3>
                                <p>Create and list new products</p>
                            </div>
                            <div className="action-card" onClick={() => setActiveTab('my-products')}>
                                <div className="action-icon">📦</div>
                                <h3>My Products</h3>
                                <p>Manage your product listings</p>
                            </div>
                            <div className="action-card">
                                <div className="action-icon">📊</div>
                                <h3>Analytics</h3>
                                <p>View performance metrics</p>
                            </div>
                            <div className="action-card">
                                <div className="action-icon">🎯</div>
                                <h3>Recommendations</h3>
                                <p>AI-powered suggestions</p>
                            </div>
                        </div>
                    </div>
                );
        }
    };

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">Dashboard</h1>
                <p className="page-subtitle">Welcome to your B2B marketplace dashboard</p>
            </div>

            <div className="dashboard-tabs">
                <button
                    className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveTab('dashboard')}
                >
                    Overview
                </button>
                <button
                    className={`tab-btn ${activeTab === 'add-product' ? 'active' : ''}`}
                    onClick={() => setActiveTab('add-product')}
                >
                    Add Product
                </button>
                <button
                    className={`tab-btn ${activeTab === 'my-products' ? 'active' : ''}`}
                    onClick={() => setActiveTab('my-products')}
                >
                    My Products
                </button>
            </div>

            {renderContent()}
            {editingProduct && (
                <EditProduct
                    product={editingProduct}
                    onUpdated={handleUpdated}
                    onCancel={() => setEditingProduct(null)}
                />
            )}
        </div>
    );
}

export default DashboardPage;