import { useState, useEffect } from 'react';
import axios from 'axios';
import './Analytics.css';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';


function Analytics() {
    const [analytics, setAnalytics] = useState({
        totalSpent: 0,
        ordersCount: 0,
        avgOrderValue: 0,
        topCategories: [],
        monthlyTrends: [],
        savings: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get(`${API_BASE_URL}/analytics`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setAnalytics(res.data);
            } catch (error) {
                console.error('Error fetching analytics:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchAnalytics();
    }, []);

    if (loading) return <div className="loading">Loading analytics...</div>;

    return (
        <div className="analytics-container">
            <h1>Business Analytics Dashboard</h1>

            <div className="analytics-grid">
                <div className="metric-card">
                    <h3>Total Spent</h3>
                    <div className="metric-value">${analytics.totalSpent.toLocaleString()}</div>
                </div>

                <div className="metric-card">
                    <h3>Orders</h3>
                    <div className="metric-value">{analytics.ordersCount}</div>
                </div>

                <div className="metric-card">
                    <h3>Avg Order Value</h3>
                    <div className="metric-value">${analytics.avgOrderValue.toFixed(2)}</div>
                </div>

                <div className="metric-card">
                    <h3>Savings</h3>
                    <div className="metric-value savings">${analytics.savings.toLocaleString()}</div>
                </div>
            </div>

            <div className="analytics-sections">
                <div className="section">
                    <h2>Top Categories</h2>
                    <div className="category-list">
                        {analytics.topCategories.map((category, index) => (
                            <div key={index} className="category-item">
                                <span className="category-name">{category.name}</span>
                                <span className="category-amount">${category.amount}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="section">
                    <h2>Monthly Trends</h2>
                    <div className="trends-chart">
                        {analytics.monthlyTrends.map((trend, index) => (
                            <div key={index} className="trend-bar">
                                <div
                                    className="bar"
                                    style={{ height: `${(trend.amount / Math.max(...analytics.monthlyTrends.map(t => t.amount))) * 100}%` }}
                                ></div>
                                <span className="trend-month">{trend.month}</span>
                                <span className="trend-amount">${trend.amount}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Analytics;
