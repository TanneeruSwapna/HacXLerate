const User = require('./models/User');
const Product = require('./models/Product');
const bcrypt = require('bcryptjs');
const logger = require('./logger');

async function seed() {
  try {
    // Create a test user
    const user = await User.create({
      email: 'test@qwipo.com',
      password: bcrypt.hashSync('password', 10),
      purchaseHistory: ['Apple', 'Banana'],
      name: 'Test User',
      businessInfo: {
        companyName: 'Test Company',
        businessType: 'Retail'
      }
    });

    // Create products with the user as creator
    await Product.create([
      {
        name: 'Apple',
        price: 1,
        category: 'Fruit',
        description: 'Fresh red apples',
        createdBy: user._id
      },
      {
        name: 'Banana',
        price: 0.5,
        category: 'Fruit',
        description: 'Yellow bananas',
        createdBy: user._id
      },
      {
        name: 'Carrot',
        price: 0.8,
        category: 'Vegetable',
        description: 'Fresh orange carrots',
        createdBy: user._id
      },
      {
        name: 'Laptop Computer',
        price: 999.99,
        category: 'Electronics',
        description: 'High-performance laptop for business use',
        brand: 'TechCorp',
        createdBy: user._id,
        specifications: {
          weight: '1.5 kg',
          dimensions: '35x25x2 cm',
          material: 'Aluminum',
          color: 'Silver'
        },
        inventory: {
          quantity: 50,
          minOrderQuantity: 1,
          maxOrderQuantity: 10
        }
      },
      {
        name: 'Office Chair',
        price: 299.99,
        category: 'Furniture',
        description: 'Ergonomic office chair with lumbar support',
        brand: 'ComfortPro',
        createdBy: user._id,
        specifications: {
          weight: '15 kg',
          dimensions: '60x60x120 cm',
          material: 'Mesh and Steel',
          color: 'Black'
        },
        inventory: {
          quantity: 25,
          minOrderQuantity: 1,
          maxOrderQuantity: 5
        }
      }
    ]);

    logger.info('Data seeded successfully');
  } catch (err) {
    logger.error('Seed error:', err);
  }
}

module.exports = seed;