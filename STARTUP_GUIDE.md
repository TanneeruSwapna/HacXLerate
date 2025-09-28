# 🚀 B2B Marketplace Startup Guide

This guide will help you run the complete B2B Marketplace application with all three services: Frontend, Backend, and ML Service.

## 📋 Prerequisites

### **Required Software**
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (3.8 or higher) - [Download here](https://python.org/)
- **npm** (comes with Node.js)
- **Git** (for cloning the repository)

### **System Requirements**
- **RAM**: 8GB+ recommended
- **Storage**: 2GB+ free space
- **OS**: Windows, macOS, or Linux

## 🎯 Quick Start (Recommended)

### **Option 1: Start All Services at Once**
```bash
# Install dependencies and start all services
python run_all_services.py --install

# Or just start services (if dependencies already installed)
python run_all_services.py
```

This will:
- ✅ Check all dependencies
- 📦 Install all required packages
- 🚀 Start all services in the correct order
- 🌐 Open your browser to the application
- 📊 Show service status and URLs

## 🔧 Manual Setup (Step by Step)

### **Step 1: Clone and Navigate**
```bash
git clone <your-repository-url>
cd HacXLerate
```

### **Step 2: Start Backend Service**
```bash
# Option A: Use the startup script
python start_backend.py

# Option B: Manual commands
cd backend
npm install
npm start
```
Backend will run on: `http://localhost:5000`

### **Step 3: Start ML Service**
```bash
# Option A: Use the startup script
python start_ml_service.py

# Option B: Manual commands
cd ml-service
pip install -r requirements.txt
python enhanced_data_generator.py  # Generate sample data
python advanced_ml_server.py
```
ML Service will run on: `http://localhost:5001`

### **Step 4: Start Frontend Service**
```bash
# Option A: Use the startup script
python start_frontend.py

# Option B: Manual commands
cd frontend
npm install
npm run dev
```
Frontend will run on: `http://localhost:3000`

### **Step 5: Start Analytics Dashboard (Optional)**
```bash
cd ml-service
python analytics_dashboard.py
```
Analytics Dashboard will run on: `http://localhost:5002`

## 🌐 Service URLs

Once all services are running, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Main Application** | http://localhost:3000 | Frontend React app |
| **Backend API** | http://localhost:5000 | Node.js backend |
| **ML Service** | http://localhost:5001 | AI recommendations |
| **Analytics Dashboard** | http://localhost:5002 | ML analytics |

## 🔍 Verification

### **Check Service Health**
```bash
# Backend health
curl http://localhost:5000/health

# ML service health
curl http://localhost:5001/health

# Test ML recommendations
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "history": [123, 456], "n_recommendations": 10}'
```

### **Expected Response**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "models_loaded": ["ncf", "lightfm", "xgboost", "implicit"]
}
```

## 🛠 Troubleshooting

### **Common Issues**

#### **1. Port Already in Use**
```bash
# Find process using port 3000
netstat -ano | findstr :3000

# Kill process (Windows)
taskkill /PID <PID> /F

# Kill process (Linux/Mac)
kill -9 <PID>
```

#### **2. Node.js Not Found**
```bash
# Install Node.js from https://nodejs.org/
# Or use a version manager like nvm
nvm install 18
nvm use 18
```

#### **3. Python Dependencies Issues**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r ml-service/requirements.txt
```

#### **4. MongoDB Connection Issues**
```bash
# Start MongoDB (if using local instance)
mongod

# Or use MongoDB Atlas (cloud)
# Update connection string in backend/.env
```

#### **5. ML Model Training Fails**
```bash
# Check if data exists
ls ml-service/data/

# Generate data if missing
cd ml-service
python enhanced_data_generator.py

# Train models manually
curl -X POST http://localhost:5001/train
```

### **Service-Specific Issues**

#### **Frontend Issues**
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check React version compatibility

#### **Backend Issues**
- Check MongoDB connection
- Verify environment variables in `.env`
- Check CORS settings for frontend connection

#### **ML Service Issues**
- Ensure sufficient RAM (8GB+ recommended)
- Check Python version (3.8+)
- Verify all ML packages are installed
- Check data files exist in `ml-service/data/`

## 📊 Service Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   ML Service    │
│   (React)       │◄──►│   (Node.js)     │◄──►│   (Python)      │
│   Port: 3000    │    │   Port: 5000    │    │   Port: 5001    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   MongoDB       │    │   Analytics     │
│   (User)        │    │   Database      │    │   Dashboard     │
│                 │    │                 │    │   Port: 5002    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 Development Workflow

### **1. First Time Setup**
```bash
# Clone repository
git clone <repository-url>
cd HacXLerate

# Install all dependencies and start services
python run_all_services.py --install
```

### **2. Daily Development**
```bash
# Start all services
python run_all_services.py

# Or start individual services
python start_backend.py
python start_ml_service.py
python start_frontend.py
```

### **3. Testing**
```bash
# Test ML service
python ml-service/test_ml_service.py

# Test all services
python run_all_services.py
# Then visit http://localhost:3000
```

### **4. Stopping Services**
- Press `Ctrl+C` in each terminal
- Or use the master script which stops all services

## 🔧 Configuration

### **Environment Variables**

#### **Backend (.env)**
```env
PORT=5000
MONGODB_URI=mongodb://localhost:27017/qwipo
JWT_SECRET=your-secret-key
NODE_ENV=development
```

#### **ML Service**
```python
# In advanced_ml_server.py
REDIS_HOST=localhost
REDIS_PORT=6379
EMBEDDING_SIZE=64
BATCH_SIZE=64
LEARNING_RATE=0.001
```

### **Custom Ports**
If you need to change ports:

#### **Frontend (package.json)**
```json
{
  "scripts": {
    "dev": "vite --port 3000"
  }
}
```

#### **Backend (index.js)**
```javascript
const PORT = process.env.PORT || 5000;
```

#### **ML Service (advanced_ml_server.py)**
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📱 Mobile Development

### **React Native Setup**
```bash
cd frontend
npx react-native init QwipoMobile
# Copy components and adapt for mobile
```

### **PWA Support**
```bash
cd frontend
npm install -g @vitejs/plugin-pwa
# Configure PWA in vite.config.js
```

## 🚀 Production Deployment

### **Docker Deployment**
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### **Cloud Deployment**
- **Frontend**: Vercel, Netlify, or AWS S3
- **Backend**: Heroku, AWS EC2, or Google Cloud
- **ML Service**: AWS Lambda, Google Cloud Functions, or Azure Functions
- **Database**: MongoDB Atlas or AWS DocumentDB

## 📞 Support

### **Getting Help**
1. Check this guide first
2. Review error logs in terminal
3. Check service health endpoints
4. Verify all prerequisites are installed
5. Create an issue on GitHub

### **Useful Commands**
```bash
# Check Node.js version
node --version

# Check Python version
python --version

# Check npm version
npm --version

# Check running processes
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Kill all Node.js processes
taskkill /IM node.exe /F

# Clear npm cache
npm cache clean --force
```

## 🎉 Success!

Once all services are running, you should see:
- ✅ Frontend at http://localhost:3000
- ✅ Backend API at http://localhost:5000
- ✅ ML Service at http://localhost:5001
- ✅ Analytics at http://localhost:5002

The application will automatically open in your browser, and you can start using the B2B marketplace with AI-powered recommendations!

---

**Happy Coding! 🚀**
