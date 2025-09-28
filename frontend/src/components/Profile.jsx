import { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css';

function Profile() {
    const [user, setUser] = useState(null);
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        businessInfo: {
            companyName: '',
            businessType: '',
            industry: '',
            businessSize: '',
            taxId: '',
            address: {
                street: '',
                city: '',
                state: '',
                zipCode: '',
                country: ''
            }
        },
        preferences: {
            categories: [],
            priceRange: { min: 0, max: 10000 },
            preferredBrands: [],
            notificationSettings: {
                email: true,
                sms: false,
                push: true
            }
        }
    });

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:5000/api/user/profile', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUser(res.data);
                setFormData(res.data);
            } catch (error) {
                console.error('Error fetching user profile:', error);
            }
        };
        fetchUser();
    }, []);

    const handleSave = async () => {
        try {
            const token = localStorage.getItem('token');
            await axios.put('http://localhost:5000/api/user/profile', formData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setUser(formData);
            setEditing(false);
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    };

    const handleCancel = () => {
        // Revert any changes made while editing
        setFormData(user);
        setEditing(false);
    };

    const handleInputChange = (path, value) => {
        const keys = path.split('.');
        const newData = { ...formData };
        let current = newData;

        for (let i = 0; i < keys.length - 1; i++) {
            current = current[keys[i]];
        }
        current[keys[keys.length - 1]] = value;

        setFormData(newData);
    };

    if (!user) return <div className="loading">Loading profile...</div>;

    return (
        <div className="profile-container">
            <div className="profile-header">
                <h1>Business Profile</h1>
                <div className="profile-actions">
                    {!editing && (
                        <button className="edit-btn" onClick={() => setEditing(true)}>
                            Edit Profile
                        </button>
                    )}
                    {editing && (
                        <>
                            <button className="save-btn" onClick={handleSave}>
                                Save Changes
                            </button>
                            <button className="cancel-btn" onClick={handleCancel}>
                                Cancel
                            </button>
                        </>
                    )}
                </div>
            </div>

            <div className="profile-sections">
                <div className="section">
                    <h2>Business Information</h2>
                    <div className="form-grid">
                        <div className="form-group">
                            <label>Company Name</label>
                            <input
                                type="text"
                                value={formData.businessInfo.companyName}
                                onChange={(e) => handleInputChange('businessInfo.companyName', e.target.value)}
                                disabled={!editing}
                            />
                        </div>

                        <div className="form-group">
                            <label>Business Type</label>
                            <select
                                value={formData.businessInfo.businessType}
                                onChange={(e) => handleInputChange('businessInfo.businessType', e.target.value)}
                                disabled={!editing}
                            >
                                <option value="retailer">Retailer</option>
                                <option value="wholesaler">Wholesaler</option>
                                <option value="distributor">Distributor</option>
                                <option value="manufacturer">Manufacturer</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Industry</label>
                            <input
                                type="text"
                                value={formData.businessInfo.industry}
                                onChange={(e) => handleInputChange('businessInfo.industry', e.target.value)}
                                disabled={!editing}
                            />
                        </div>

                        <div className="form-group">
                            <label>Business Size</label>
                            <select
                                value={formData.businessInfo.businessSize}
                                onChange={(e) => handleInputChange('businessInfo.businessSize', e.target.value)}
                                disabled={!editing}
                            >
                                <option value="small">Small (1-10 employees)</option>
                                <option value="medium">Medium (11-50 employees)</option>
                                <option value="large">Large (51-200 employees)</option>
                                <option value="enterprise">Enterprise (200+ employees)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div className="section">
                    <h2>Preferences</h2>
                    <div className="form-grid">
                        <div className="form-group">
                            <label>Price Range</label>
                            <div className="price-range">
                                <input
                                    type="number"
                                    placeholder="Min"
                                    value={formData.preferences.priceRange.min}
                                    onChange={(e) => handleInputChange('preferences.priceRange.min', parseInt(e.target.value))}
                                    disabled={!editing}
                                />
                                <span>to</span>
                                <input
                                    type="number"
                                    placeholder="Max"
                                    value={formData.preferences.priceRange.max}
                                    onChange={(e) => handleInputChange('preferences.priceRange.max', parseInt(e.target.value))}
                                    disabled={!editing}
                                />
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Notification Settings</label>
                            <div className="checkbox-group">
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={formData.preferences.notificationSettings.email}
                                        onChange={(e) => handleInputChange('preferences.notificationSettings.email', e.target.checked)}
                                        disabled={!editing}
                                    />
                                    Email Notifications
                                </label>
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={formData.preferences.notificationSettings.sms}
                                        onChange={(e) => handleInputChange('preferences.notificationSettings.sms', e.target.checked)}
                                        disabled={!editing}
                                    />
                                    SMS Notifications
                                </label>
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={formData.preferences.notificationSettings.push}
                                        onChange={(e) => handleInputChange('preferences.notificationSettings.push', e.target.checked)}
                                        disabled={!editing}
                                    />
                                    Push Notifications
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;
