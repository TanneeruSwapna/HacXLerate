import './AnalyticsPage.css';

function AnalyticsPage() {
    const stats = [
        { label: 'Total Revenue', value: '$12,450', change: '+12%', icon: '💰' },
        { label: 'Orders', value: '156', change: '+8%', icon: '📦' },
        { label: 'Customers', value: '89', change: '+15%', icon: '👥' },
        { label: 'Products', value: '24', change: '+3%', icon: '📊' }
    ];

    const topProducts = [
        { name: 'Office Chair Pro', sales: 45, revenue: '$13,455' },
        { name: 'Wireless Mouse', sales: 32, revenue: '$1,599' },
        { name: 'Desk Lamp LED', sales: 28, revenue: '$2,239' },
        { name: 'Keyboard Mechanical', sales: 24, revenue: '$1,199' }
    ];

    return (
        <div className="page-container">
            <div className="page-header">
                <h1 className="page-title">Analytics</h1>
                <p className="page-subtitle">Track your business performance and insights</p>
            </div>

            {/* Stats Grid */}
            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <div key={index} className="stat-card">
                        <div className="stat-icon">{stat.icon}</div>
                        <div className="stat-content">
                            <div className="stat-value">{stat.value}</div>
                            <div className="stat-label">{stat.label}</div>
                            <div className="stat-change positive">{stat.change}</div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Charts Section */}
            <div className="grid grid-2">
                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Revenue Trend</h3>
                    </div>
                    <div className="card-body">
                        <div className="chart-placeholder">
                            <div className="chart-icon">📈</div>
                            <p>Revenue chart would be displayed here</p>
                        </div>
                    </div>
                </div>

                <div className="card">
                    <div className="card-header">
                        <h3 className="card-title">Orders by Category</h3>
                    </div>
                    <div className="card-body">
                        <div className="chart-placeholder">
                            <div className="chart-icon">🥧</div>
                            <p>Pie chart would be displayed here</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Top Products */}
            <div className="card">
                <div className="card-header">
                    <h3 className="card-title">Top Selling Products</h3>
                </div>
                <div className="card-body">
                    <div className="products-table">
                        <div className="table-header">
                            <div className="table-cell">Product</div>
                            <div className="table-cell">Sales</div>
                            <div className="table-cell">Revenue</div>
                        </div>
                        {topProducts.map((product, index) => (
                            <div key={index} className="table-row">
                                <div className="table-cell">{product.name}</div>
                                <div className="table-cell">{product.sales}</div>
                                <div className="table-cell">{product.revenue}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default AnalyticsPage;