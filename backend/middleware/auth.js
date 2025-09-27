const jwt = require('jsonwebtoken');
const logger = require('../logger');

const auth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).send('Unauthorized');
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.userId = decoded.userId;
    next();
  } catch (err) {
    logger.error('Invalid token:', err);
    res.status(401).send('Invalid token');
  }
};

module.exports = auth;