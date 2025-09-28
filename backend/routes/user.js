const express = require('express');
const User = require('../models/User');
const auth = require('../middleware/auth');

const router = express.Router();

// Get user profile
router.get('/profile', auth, async (req, res, next) => {
    try {
        const user = await User.findById(req.userId).select('-password');
        res.json(user);
    } catch (err) {
        next(err);
    }
});

// Update user profile
router.put('/profile', auth, async (req, res, next) => {
    try {
        const { businessInfo, preferences } = req.body;

        const user = await User.findByIdAndUpdate(
            req.userId,
            {
                businessInfo: { ...user.businessInfo, ...businessInfo },
                preferences: { ...user.preferences, ...preferences },
                updatedAt: new Date()
            },
            { new: true, runValidators: true }
        ).select('-password');

        res.json(user);
    } catch (err) {
        next(err);
    }
});

module.exports = router;
