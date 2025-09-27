const express = require('express');
const Joi = require('joi');
const Cart = require('../models/Cart');
const auth = require('../middleware/auth');
const logger = require('../logger');

const router = express.Router();

const addItemSchema = Joi.object({
  productId: Joi.string().required(),
  quantity: Joi.number().min(1).default(1)
});

// Get Cart
router.get('/', auth, async (req, res, next) => {
  try {
    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) cart = new Cart({ userId: req.userId, items: [] });
    res.json(cart);
  } catch (err) {
    next(err);
  }
});

// Add Item
router.post('/add', auth, async (req, res, next) => {
  const { error } = addItemSchema.validate(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  try {
    const { productId, quantity } = req.body;
    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) cart = new Cart({ userId: req.userId, items: [] });

    const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
    if (itemIndex > -1) {
      cart.items[itemIndex].quantity += quantity;
    } else {
      cart.items.push({ productId, quantity });
    }
    await cart.save();
    logger.info(`Item added to cart for user ${req.userId}`);
    res.json(cart);
  } catch (err) {
    next(err);
  }
});

// Could add update/remove routes similarly

module.exports = router;