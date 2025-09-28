import { useState, useEffect } from 'react';
import './ProfilePage.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


function ProfilePage() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const userData = localStorage.getItem('user');
        if (userData) {
            setUser(JSON.parse(userData));
        }
    }, []);

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">Profile</h1>
                <p className="page-subtitle">Manage your account settings</p>
            </div>

            <div className="grid grid-2">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Account Information</h3>
                    </div>
                    <div className="card-body">
                        <div className="profile-info">
                            <div className="info-item">
                                <label>Email</label>
                                <span>{user?.email || 'Not available'}</span>
                            </div>
                            <div className="info-item">
                                <label>Name</label>
                                <span>{user?.name || 'Not available'}</span>
                            </div>
                            <div className="info-item">
                                <label>Company</label>
                                <span>{user?.businessInfo?.companyName || 'Not available'}</span>
                            </div>
                            <div className="info-item">
                                <label>Business Type</label>
                                <span>{user?.businessInfo?.businessType || 'Not available'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Quick Stats</h3>
                    </div>
                    <div className="card-body">
                        <div className="stats-grid">
                            <div className="stat-item">
                                <div className="stat-value">24</div>
                                <div className="stat-label">Products</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-value">156</div>
                                <div className="stat-label">Orders</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-value">89</div>
                                <div className="stat-label">Customers</div>
                            </div>
                            <div className="stat-item">
                                <div className="stat-value">$12K</div>
                                <div className="stat-label">Revenue</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;