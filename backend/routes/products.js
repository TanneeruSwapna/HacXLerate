const express = require('express');
const Product = require('../models/Product');
const auth = require('../middleware/auth');

const router = express.Router();

// Get all products with user information
router.get('/', auth, async (req, res, next) => {
  try {
    const products = await Product.find({ isActive: true }).populate('createdBy', 'name email');
    res.json(products);
  } catch (err) {
    next(err);
  }
});

// Create a new product
router.post('/', auth, async (req, res, next) => {
  try {
    const productData = {
      ...req.body,
      createdBy: req.userId
    };

    // Generate SKU if not provided
    if (!productData.sku) {
      const timestamp = Date.now().toString(36);
      const random = Math.random().toString(36).substr(2, 5);
      productData.sku = `PROD-${timestamp}-${random}`.toUpperCase();
    }

    const product = new Product(productData);
    await product.save();

    // Populate the createdBy field for the response
    await product.populate('createdBy', 'name email');

    res.status(201).json(product);
  } catch (err) {
    if (err.code === 11000) {
      res.status(400).json({ error: 'SKU already exists' });
    } else {
      next(err);
    }
  }
});

// Get products created by the authenticated user
router.get('/my-products', auth, async (req, res, next) => {
  try {
    const products = await Product.find({ createdBy: req.userId }).populate('createdBy', 'name email');
    res.json(products);
  } catch (err) {
    next(err);
  }
});

// Update a product (only by the creator)
router.put('/:id', auth, async (req, res, next) => {
  try {
    const product = await Product.findOne({ _id: req.params.id, createdBy: req.userId });

    if (!product) {
      return res.status(404).json({ error: 'Product not found or not authorized to update' });
    }

    const updatedProduct = await Product.findByIdAndUpdate(
      req.params.id,
      { ...req.body, updatedAt: new Date() },
      { new: true, runValidators: true }
    ).populate('createdBy', 'name email');

    res.json(updatedProduct);
  } catch (err) {
    next(err);
  }
});

// Delete a product (only by the creator)
router.delete('/:id', auth, async (req, res, next) => {
  try {
    const product = await Product.findOne({ _id: req.params.id, createdBy: req.userId });

    if (!product) {
      return res.status(404).json({ error: 'Product not found or not authorized to delete' });
    }

    await Product.findByIdAndDelete(req.params.id);
    res.json({ message: 'Product deleted successfully' });
  } catch (err) {
    next(err);
  }
});

module.exports = router;