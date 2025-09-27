const express = require('express');
const axios = require('axios');
const User = require('../models/User');
const auth = require('../middleware/auth');
const logger = require('../logger');
const io = require('socket.io'); // Note: io is global in index, but for simplicity, assume passed or use event emitter if needed

const router = express.Router();

router.get('/', auth, async (req, res, next) => {
  try {
    const user = await User.findById(req.userId);
    const mlRes = await axios.post('http://localhost:5001/predict', { history: user.purchaseHistory });
    let recs = mlRes.data.recommendations;

    const geminiRes = await axios.post(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${process.env.GEMINI_API_KEY}`, {
      contents: [{ parts: [{ text: `Generate reasons for these product recommendations: ${JSON.stringify(recs)}` }] }]
    });
    const geminiReasons = geminiRes.data.candidates[0].content.parts[0].text || '';
    recs = recs.map((rec, i) => ({ ...rec, reason: geminiReasons.split('\n')[i] || 'No reason available' }));

    // Emit (assuming io is accessible; in prod, use Redis for cluster)
    // io.emit('new-recommendation', recs[0]); // For cluster, need pub/sub

    res.json(recs);
  } catch (err) {
    logger.error('Recommendations error:', err);
    next(err);
  }
});

module.exports = router;