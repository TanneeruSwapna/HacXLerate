import { useState, useEffect } from 'react';
import axios from 'axios';
import './AddProduct.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


function EditProduct({ product, onUpdated, onCancel }) {
    const [formData, setFormData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (product) {
            // Clone and normalize product into form shape
            setFormData({
                name: product.name || '',
                description: product.description || '',
                price: product.price ?? '',
                category: product.category || '',
                subcategory: product.subcategory || '',
                brand: product.brand || '',
                images: product.images ? [...product.images] : [],
                specifications: {
                    weight: product.specifications?.weight || '',
                    dimensions: product.specifications?.dimensions || '',
                    material: product.specifications?.material || '',
                    color: product.specifications?.color || ''
                },
                inventory: {
                    quantity: product.inventory?.quantity ?? 0,
                    minOrderQuantity: product.inventory?.minOrderQuantity ?? 1,
                    maxOrderQuantity: product.inventory?.maxOrderQuantity ?? '',
                    reorderPoint: product.inventory?.reorderPoint ?? ''
                },
                pricing: {
                    wholesale: product.pricing?.wholesale ?? '',
                    retail: product.pricing?.retail ?? ''
                },
                tags: product.tags ? [...product.tags] : []
            });
        }
    }, [product]);

    if (!product || !formData) return null;

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        if (name.includes('.')) {
            const [parent, child] = name.split('.');
            setFormData((prev) => ({
                ...prev,
                [parent]: {
                    ...prev[parent],
                    [child]: value
                }
            }));
        } else {
            setFormData((prev) => ({ ...prev, [name]: value }));
        }
    };

    const handleImageUrlChange = (index, value) => {
        const newImages = [...formData.images];
        newImages[index] = value;
        setFormData((prev) => ({ ...prev, images: newImages }));
    };

    const addImageUrl = () => setFormData((prev) => ({ ...prev, images: [...prev.images, ''] }));
    const removeImageUrl = (index) => setFormData((prev) => ({ ...prev, images: prev.images.filter((_, i) => i !== index) }));

    const handleTagsChange = (e) => {
        const tags = e.target.value.split(',').map((t) => t.trim()).filter(Boolean);
        setFormData((prev) => ({ ...prev, tags }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
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
                images: formData.images.filter((img) => img && img.trim())
            };

            await axios.put(`${API_BASE_URL}/products/${product._id}`, submitData, {
                headers: { Authorization: `Bearer ${token}` }
            });

            onUpdated();
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to update product');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="edit-product-modal">
            <div className="modal-card">
                <div className="modal-header flex-between">
                    <h3>Edit Product</h3>
                    <button className="btn btn-secondary" onClick={onCancel}>Close</button>
                </div>

                {error && <div className="alert alert-error">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="card-body">
                        <div className="form-section">
                            <label className="form-label">Product Name *</label>
                            <input name="name" value={formData.name} onChange={handleInputChange} className="form-input" required />
                        </div>

                        <div className="form-section">
                            <label className="form-label">Price *</label>
                            <input name="price" type="number" step="0.01" min="0" value={formData.price} onChange={handleInputChange} className="form-input" required />
                        </div>

                        <div className="form-section">
                            <label className="form-label">Description</label>
                            <textarea name="description" value={formData.description} onChange={handleInputChange} className="form-textarea" rows="3" />
                        </div>

                        <div className="form-section">
                            <label className="form-label">Category</label>
                            <input name="category" value={formData.category} onChange={handleInputChange} className="form-input" />
                        </div>

                        <div className="form-section">
                            <h4>Images</h4>
                            {formData.images.map((image, index) => (
                                <div key={index} className="form-group">
                                    <input type="url" value={image} onChange={(e) => handleImageUrlChange(index, e.target.value)} className="form-input" />
                                    <button type="button" className="btn btn-danger" onClick={() => removeImageUrl(index)}>Remove</button>
                                </div>
                            ))}
                            <button type="button" className="btn btn-secondary" onClick={addImageUrl}>Add Image URL</button>
                        </div>

                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary" disabled={loading}>{loading ? 'Saving...' : 'Save Changes'}</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default EditProduct;
