const request = require('supertest');
const app = require('../index'); // Adjust if needed; for testing, export app

describe('Auth Routes', () => {
  it('should login with valid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@qwipo.com', password: 'password' });
    expect(res.statusCode).toEqual(200);
    expect(res.body).toHaveProperty('token');
  });

  it('should fail login with invalid credentials', async () => {
    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: 'wrong@qwipo.com', password: 'wrong' });
    expect(res.statusCode).toEqual(400);
  });
});