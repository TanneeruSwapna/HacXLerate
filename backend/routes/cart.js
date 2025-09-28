const express = require('express');
const Joi = require('joi');
const Cart = require('../models/Cart');
const Product = require('../models/Product');
const auth = require('../middleware/auth');
const logger = require('../logger');

const router = express.Router();

const addItemSchema = Joi.object({
  productId: Joi.string().required(),
  quantity: Joi.number().min(1).default(1)
});

const updateItemSchema = Joi.object({
  productId: Joi.string().required(),
  quantity: Joi.number().min(0).required() // 0 will remove the item
});

// Helper to extract productId from various places and normalize IDs
function extractProductId(req) {
  return req.params?.productId || req.body?.productId || req.query?.productId;
}

function itemProductId(item) {
  // item.productId may be an ObjectId, a string, or a populated object with _id
  if (!item) return '';
  if (item._id) return String(item._id); // in case a product-like object passed
  if (item.productId && item.productId._id) return String(item.productId._id);
  if (item.productId) return String(item.productId);
  return '';
}

// Get Cart
router.get('/', auth, async (req, res, next) => {
  try {
    let cart = await Cart.findOne({ userId: req.userId }).populate('items.productId', 'name price images category sku inventory');
    if (!cart) {
      cart = new Cart({ userId: req.userId, items: [] });
      await cart.save();
      cart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');
    }
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
    // First, try to decrement product inventory atomically if enough stock exists
    const updatedProduct = await Product.findOneAndUpdate(
      { _id: productId, 'inventory.quantity': { $gte: quantity } },
      { $inc: { 'inventory.quantity': -quantity } },
      { new: true }
    );

    if (!updatedProduct) {
      return res.status(400).json({ error: 'Insufficient stock for this product' });
    }

    // Then add to cart
    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) cart = new Cart({ userId: req.userId, items: [] });

    const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
    if (itemIndex > -1) {
      cart.items[itemIndex].quantity += quantity;
    } else {
      cart.items.push({ productId, quantity });
    }

    try {
      await cart.save();
      // Re-query and populate to ensure clean populated response
      const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');
      logger.info(`Item added to cart for user ${req.userId}`);
      return res.json(fullCart);
    } catch (saveErr) {
      // Rollback inventory decrement if saving cart failed
      try {
        await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': quantity } });
      } catch (rollbackErr) {
        logger.error('Failed to rollback product inventory after cart save failure', rollbackErr);
      }
      throw saveErr;
    }
  } catch (err) {
    next(err);
  }
});

// Could add update/remove routes similarly

// Update item quantity in cart (quantity = 0 removes the item)
router.put('/update', auth, async (req, res, next) => {
  const { error } = updateItemSchema.validate(req.body);
  if (error) return res.status(400).send(error.details[0].message);

  try {
    const { productId, quantity } = req.body;
    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) return res.status(404).json({ error: 'Cart not found' });

    const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
    if (itemIndex === -1) return res.status(404).json({ error: 'Item not found in cart' });

    const currentQty = cart.items[itemIndex].quantity;

    if (quantity === 0) {
      // Remove item and restore inventory
      cart.items.splice(itemIndex, 1);
      await cart.save();
      const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');
      try {
        await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': currentQty } });
      } catch (rollErr) {
        logger.error('Failed to restore inventory after remove', rollErr);
      }
      logger.info(`Item removed from cart for user ${req.userId}`);
      return res.json(fullCart);
    }

    if (quantity > currentQty) {
      // Need to reserve more stock: decrement inventory by delta
      const delta = quantity - currentQty;
      const updatedProduct = await Product.findOneAndUpdate(
        { _id: productId, 'inventory.quantity': { $gte: delta } },
        { $inc: { 'inventory.quantity': -delta } },
        { new: true }
      );
      if (!updatedProduct) return res.status(400).json({ error: 'Insufficient stock to increase quantity' });
      cart.items[itemIndex].quantity = quantity;
    } else if (quantity < currentQty) {
      // Return inventory for the difference
      const delta = currentQty - quantity;
      try {
        await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': delta } });
      } catch (incErr) {
        logger.error('Failed to restore inventory after decreasing qty', incErr);
      }
      cart.items[itemIndex].quantity = quantity;
    }

    await cart.save();
    const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');
    logger.info(`Cart updated for user ${req.userId}`);
    res.json(fullCart);
  } catch (err) {
    next(err);
  }
});

// Remove an item from cart and restore inventory
router.delete('/remove', auth, async (req, res, next) => {
  try {
    const productId = extractProductId(req);
    if (!productId) return res.status(400).json({ error: 'productId is required' });

    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) return res.status(404).json({ error: 'Cart not found' });

    const itemIndex = cart.items.findIndex(item => {
      const id = itemProductId(item) || String(item.productId || '');
      return id === String(productId);
    });
    if (itemIndex === -1) return res.status(404).json({ error: 'Item not found in cart' });

    const removed = cart.items.splice(itemIndex, 1)[0];
    await cart.save();
    const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');

    try {
      await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': removed.quantity } });
    } catch (err) {
      logger.error('Failed to restore inventory after remove', err);
    }

    logger.info(`Item removed from cart for user ${req.userId}`);
    res.json(fullCart);
  } catch (err) {
    next(err);
  }
});
// Accept POST /remove (some clients/proxies don't send bodies with DELETE)
router.post('/remove', auth, async (req, res, next) => {
  try {
    const productId = extractProductId(req);
    logger.info('POST /api/cart/remove called with', { productId, userId: req.userId });
    if (!productId) return res.status(400).json({ error: 'productId is required' });

    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) return res.status(404).json({ error: 'Cart not found' });

    const itemIndex = cart.items.findIndex(item => itemProductId(item) === String(productId));
    if (itemIndex === -1) return res.status(404).json({ error: 'Item not found in cart' });

    const removed = cart.items.splice(itemIndex, 1)[0];
    await cart.save();
    const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');

    try {
      await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': removed.quantity } });
    } catch (err) {
      logger.error('Failed to restore inventory after remove (POST)', err);
    }

    logger.info(`Item removed from cart (POST) for user ${req.userId}`);
    res.json(fullCart);
  } catch (err) {
    next(err);
  }
});

// Accept DELETE /remove/:productId as alternative
router.delete('/remove/:productId', auth, async (req, res, next) => {
  try {
    const productId = req.params.productId;
    logger.info('DELETE /api/cart/remove/:productId called with', { productId, userId: req.userId });
    if (!productId) return res.status(400).json({ error: 'productId is required' });

    let cart = await Cart.findOne({ userId: req.userId });
    if (!cart) return res.status(404).json({ error: 'Cart not found' });

    const itemIndex = cart.items.findIndex(item => item.productId.toString() === productId);
    if (itemIndex === -1) return res.status(404).json({ error: 'Item not found in cart' });

    const removed = cart.items.splice(itemIndex, 1)[0];
    await cart.save();
    const fullCart = await Cart.findById(cart._id).populate('items.productId', 'name price images category sku inventory');

    try {
      await Product.findByIdAndUpdate(productId, { $inc: { 'inventory.quantity': removed.quantity } });
    } catch (err) {
      logger.error('Failed to restore inventory after remove (DELETE param)', err);
    }

    logger.info(`Item removed from cart (DELETE param) for user ${req.userId}`);
    res.json(fullCart);
  } catch (err) {
    next(err);
  }
});

module.exports = router;