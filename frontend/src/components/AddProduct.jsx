import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './AddProduct.css';

function AddProduct() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        price: '',
        category: '',
        subcategory: '',
        brand: '',
        images: [],
        specifications: {
            weight: '',
            dimensions: '',
            material: '',
            color: ''
        },
        inventory: {
            quantity: 0,
            minOrderQuantity: 1,
            maxOrderQuantity: '',
            reorderPoint: ''
        },
        pricing: {
            wholesale: '',
            retail: ''
        },
        tags: []
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const categories = [
        'Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors',
        'Books', 'Toys & Games', 'Health & Beauty', 'Automotive',
        'Food & Beverages', 'Office Supplies', 'Other'
    ];

    const handleInputChange = (e) => {
        const { name, value } = e.target;

        if (name.includes('.')) {
            const [parent, child] = name.split('.');
            setFormData(prev => ({
                ...prev,
                [parent]: {
                    ...prev[parent],
                    [child]: value
                }
            }));
        } else {
            setFormData(prev => ({
                ...prev,
                [name]: value
            }));
        }
    };

    const handleImageUrlChange = (index, value) => {
        const newImages = [...formData.images];
        newImages[index] = value;
        setFormData(prev => ({
            ...prev,
            images: newImages
        }));
    };

    const addImageUrl = () => {
        setFormData(prev => ({
            ...prev,
            images: [...prev.images, '']
        }));
    };

    const removeImageUrl = (index) => {
        setFormData(prev => ({
            ...prev,
            images: prev.images.filter((_, i) => i !== index)
        }));
    };

    const handleTagsChange = (e) => {
        const tags = e.target.value.split(',').map(tag => tag.trim()).filter(tag => tag);
        setFormData(prev => ({
            ...prev,
            tags
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        try {
            const token = localStorage.getItem('token');

            // Prepare data for submission
            const submitData = {
                ...formData,
                price: parseFloat(formData.price),
                inventory: {
                    ...formData.inventory,
                    quantity: parseInt(formData.inventory.quantity),
                    minOrderQuantity: parseInt(formData.inventory.minOrderQuantity),
                    maxOrderQuantity: formData.inventory.maxOrderQuantity ? parseInt(formData.inventory.maxOrderQuantity) : undefined,
                    reorderPoint: formData.inventory.reorderPoint ? parseInt(formData.inventory.reorderPoint) : undefined
                },
                pricing: {
                    wholesale: formData.pricing.wholesale ? parseFloat(formData.pricing.wholesale) : undefined,
                    retail: formData.pricing.retail ? parseFloat(formData.pricing.retail) : undefined
                },
                images: formData.images.filter(img => img.trim())
            };

            await axios.post('http://localhost:5000/api/products', submitData, {
                headers: { Authorization: `Bearer ${token}` }
            });

            setSuccess('Product created successfully!');
            navigate('/products');
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to create product');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <div className="page-header">
                <div className="flex-between">
                    <div>
                        <h1 className="page-title">Add New Product</h1>
                        <p className="page-subtitle">Create a new product for your catalog</p>
                    </div>
                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate('/products')}
                    >
                        Back to Products
                    </button>
                </div>
            </div>

            {error && <div className="alert alert-error">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}

            <div className="card">
                <form onSubmit={handleSubmit}>
                    <div className="card-body">
                        {/* Basic Information */}
                        <div className="form-section">
                            <h3 className="section-title">Basic Information</h3>
                            <div className="grid grid-2">
                                <div className="form-group">
                                    <label className="form-label">Product Name *</label>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Price *</label>
                                    <input
                                        type="number"
                                        name="price"
                                        value={formData.price}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        step="0.01"
                                        min="0"
                                        required
                                    />
                                </div>
                            </div>
                            <div className="form-group">
                                <label className="form-label">Description</label>
                                <textarea
                                    name="description"
                                    value={formData.description}
                                    onChange={handleInputChange}
                                    className="form-textarea"
                                    rows="3"
                                />
                            </div>
                            <div className="grid grid-2">
                                <div className="form-group">
                                    <label className="form-label">Category *</label>
                                    <select
                                        name="category"
                                        value={formData.category}
                                        onChange={handleInputChange}
                                        className="form-select"
                                        required
                                    >
                                        <option value="">Select Category</option>
                                        {categories.map(cat => (
                                            <option key={cat} value={cat}>{cat}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Brand</label>
                                    <input
                                        type="text"
                                        name="brand"
                                        value={formData.brand}
                                        onChange={handleInputChange}
                                        className="form-input"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Images */}
                        <div className="form-section">
                            <h3 className="section-title">Images</h3>
                            {formData.images.map((image, index) => (
                                <div key={index} className="form-group">
                                    <label className="form-label">Image URL {index + 1}</label>
                                    <div className="flex gap-2">
                                        <input
                                            type="url"
                                            value={image}
                                            onChange={(e) => handleImageUrlChange(index, e.target.value)}
                                            placeholder="https://example.com/image.jpg"
                                            className="form-input"
                                            style={{ flex: 1 }}
                                        />
                                        <button
                                            type="button"
                                            className="btn btn-danger"
                                            onClick={() => removeImageUrl(index)}
                                        >
                                            Remove
                                        </button>
                                    </div>
                                </div>
                            ))}
                            <button type="button" className="btn btn-secondary" onClick={addImageUrl}>
                                Add Image URL
                            </button>
                        </div>

                        {/* Inventory */}
                        <div className="form-section">
                            <h3 className="section-title">Inventory</h3>
                            <div className="grid grid-2">
                                <div className="form-group">
                                    <label className="form-label">Quantity in Stock</label>
                                    <input
                                        type="number"
                                        name="inventory.quantity"
                                        value={formData.inventory.quantity}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        min="0"
                                    />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Minimum Order Quantity</label>
                                    <input
                                        type="number"
                                        name="inventory.minOrderQuantity"
                                        value={formData.inventory.minOrderQuantity}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        min="1"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Pricing */}
                        <div className="form-section">
                            <h3 className="section-title">Pricing</h3>
                            <div className="grid grid-2">
                                <div className="form-group">
                                    <label className="form-label">Wholesale Price</label>
                                    <input
                                        type="number"
                                        name="pricing.wholesale"
                                        value={formData.pricing.wholesale}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        step="0.01"
                                        min="0"
                                    />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Retail Price</label>
                                    <input
                                        type="number"
                                        name="pricing.retail"
                                        value={formData.pricing.retail}
                                        onChange={handleInputChange}
                                        className="form-input"
                                        step="0.01"
                                        min="0"
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary" disabled={loading}>
                                {loading ? 'Creating...' : 'Create Product'}
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default AddProduct;