const express = require('express');
const Joi = require('joi');
const User = require('../models/User');
const auth = require('../middleware/auth');
const logger = require('../logger');

const router = express.Router();

const purchaseSchema = Joi.object({
  product: Joi.string().required()
});

router.post('/', auth, async (req, res, next) => {
  const { error } = purchaseSchema.validate(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  try {
    const { product } = req.body;
    const user = await User.findById(req.userId);
    user.purchaseHistory.push(product);
    await user.save();
    logger.info(`Purchase added for user ${req.userId}: ${product}`);
    res.json({ message: 'Purchase added' });
  } catch (err) {
    next(err);
  }
});

module.exports = router;