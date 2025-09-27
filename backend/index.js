const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const cluster = require('cluster');
const os = require('os');

const logger = require('./logger');
require('dotenv').config();

const authRoutes = require('./routes/auth');
const productsRoutes = require('./routes/products');
const recommendationsRoutes = require('./routes/recommendations');
const purchasesRoutes = require('./routes/purchases');
const cartRoutes = require('./routes/cart');
const errorHandler = require('./middleware/errorHandler');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;
  logger.info(`Master ${process.pid} is running. Forking ${numCPUs} workers...`);
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
  cluster.on('exit', (worker, code, signal) => {
    logger.error(`Worker ${worker.process.pid} died. Forking new...`);
    cluster.fork();
  });
} else {
  const app = express();
  const http = require('http');
  const server = http.createServer(app);
  const io = require('socket.io')(server, { cors: { origin: '*' } });

  app.use(helmet()); // Security headers
  app.use(cors());
  app.use(express.json());

  // Connect to MongoDB
  mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => logger.info('MongoDB connected'))
    .catch(err => logger.error('MongoDB connection error:', err));

  // Routes
  app.use('/api/auth', authRoutes);
  app.use('/api/products', productsRoutes);
  app.use('/api/recommendations', recommendationsRoutes);
  app.use('/api/purchases', purchasesRoutes);
  app.use('/api/cart', cartRoutes);

  // Global error handler
  app.use(errorHandler);

  server.listen(5000, () => logger.info(`Worker ${process.pid} running on port 5000`));
}

