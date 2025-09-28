const express = require('express');
const User = require('../models/User');
const Product = require('../models/Product');
const auth = require('../middleware/auth');

const router = express.Router();

router.get('/stats', auth, async (req, res, next) => {
    try {
        const user = await User.findById(req.userId);

        // Calculate stats from purchase history
        const totalOrders = user.purchaseHistory.length;
        const totalSpent = user.purchaseHistory.reduce((sum, purchase) => sum + (purchase.price * purchase.quantity), 0);
        const pendingOrders = 0; // This would come from an orders collection in a real app

        res.json({
            totalOrders,
            totalSpent,
            pendingOrders
        });
    } catch (err) {
        next(err);
    }
});

module.exports = router;
