const express = require('express');
const User = require('../models/User');
const Product = require('../models/Product');
const auth = require('../middleware/auth');

const router = express.Router();

router.get('/', auth, async (req, res, next) => {
    try {
        const user = await User.findById(req.userId).populate('purchaseHistory.productId');

        // Calculate analytics
        const totalSpent = user.purchaseHistory.reduce((sum, purchase) => sum + (purchase.price * purchase.quantity), 0);
        const ordersCount = user.purchaseHistory.length;
        const avgOrderValue = ordersCount > 0 ? totalSpent / ordersCount : 0;

        // Calculate top categories
        const categorySpending = {};
        user.purchaseHistory.forEach(purchase => {
            if (purchase.productId && purchase.productId.category) {
                const category = purchase.productId.category;
                categorySpending[category] = (categorySpending[category] || 0) + (purchase.price * purchase.quantity);
            }
        });

        const topCategories = Object.entries(categorySpending)
            .map(([name, amount]) => ({ name, amount }))
            .sort((a, b) => b.amount - a.amount)
            .slice(0, 5);

        // Mock monthly trends (in a real app, this would be calculated from actual data)
        const monthlyTrends = [
            { month: 'Jan', amount: Math.floor(totalSpent * 0.8) },
            { month: 'Feb', amount: Math.floor(totalSpent * 0.9) },
            { month: 'Mar', amount: Math.floor(totalSpent * 1.1) },
            { month: 'Apr', amount: Math.floor(totalSpent * 0.95) },
            { month: 'May', amount: Math.floor(totalSpent * 1.2) },
            { month: 'Jun', amount: totalSpent }
        ];

        const savings = Math.floor(totalSpent * 0.15); // Mock 15% savings from bulk purchases

        res.json({
            totalSpent,
            ordersCount,
            avgOrderValue,
            topCategories,
            monthlyTrends,
            savings
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
