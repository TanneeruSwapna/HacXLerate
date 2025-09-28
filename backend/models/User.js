const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  businessInfo: {
    companyName: { type: String, required: true },
    businessType: { type: String, enum: ['retailer', 'wholesaler', 'distributor', 'manufacturer'] },
    industry: { type: String },
    businessSize: { type: String, enum: ['small', 'medium', 'large', 'enterprise'] },
    taxId: { type: String },
    address: {
      street: { type: String },
      city: { type: String },
      state: { type: String },
      zipCode: { type: String },
      country: { type: String }
    }
  },
  preferences: {
    categories: [{ type: String }],
    priceRange: {
      min: { type: Number },
      max: { type: Number }
    },
    preferredBrands: [{ type: String }],
    notificationSettings: {
      email: { type: Boolean, default: true },
      sms: { type: Boolean, default: false },
      push: { type: Boolean, default: true }
    }
  },
  purchaseHistory: [{
    productId: { type: mongoose.Schema.Types.ObjectId, ref: 'Product' },
    quantity: { type: Number },
    price: { type: Number },
    purchaseDate: { type: Date, default: Date.now },
    orderId: { type: String }
  }],
  wishlist: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Product' }],
  creditLimit: { type: Number, default: 10000 },
  paymentTerms: { type: String, enum: ['net30', 'net60', 'net90', 'cod'], default: 'net30' },
  isVerified: { type: Boolean, default: false },
  lastLogin: { type: Date },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', UserSchema);