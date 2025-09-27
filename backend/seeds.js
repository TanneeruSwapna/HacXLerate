const User = require('./models/User');
const Product = require('./models/Product');
const bcrypt = require('bcryptjs');
const logger = require('./logger');

async function seed() {
  try {
    await User.create({ email: 'test@qwipo.com', password: bcrypt.hashSync('password', 10), purchaseHistory: ['Apple', 'Banana'] });
    await Product.create([
      { name: 'Apple', price: 1, category: 'Fruit' },
      { name: 'Banana', price: 0.5, category: 'Fruit' },
      { name: 'Carrot', price: 0.8, category: 'Veg' }
    ]);
    logger.info('Data seeded');
  } catch (err) {
    logger.error('Seed error:', err);
  }
}

module.exports = seed;