const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String },
  price: { type: Number, required: true },
  category: { type: String, required: true },
  subcategory: { type: String },
  brand: { type: String },
  sku: { type: String, unique: true },
  images: [{ type: String }],
  specifications: {
    weight: { type: String },
    dimensions: { type: String },
    material: { type: String },
    color: { type: String }
  },
  inventory: {
    quantity: { type: Number, default: 0 },
    minOrderQuantity: { type: Number, default: 1 },
    maxOrderQuantity: { type: Number },
    reorderPoint: { type: Number }
  },
  pricing: {
    wholesale: { type: Number },
    retail: { type: Number },
    bulkDiscount: [{
      minQuantity: { type: Number },
      discountPercent: { type: Number }
    }]
  },
  tags: [{ type: String }],
  isActive: { type: Boolean, default: true },
  createdBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Product', ProductSchema);