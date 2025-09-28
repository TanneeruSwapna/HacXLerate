# 🚀 Quick Start Guide - B2B Marketplace

## ⚡ Fastest Way to Get Started

### **Step 1: Install Dependencies**
```bash
# Install minimal ML dependencies (compatible with Python 3.12)
cd ml-service
pip install -r minimal_requirements.txt

# Install backend dependencies
cd ../backend
npm install

# Install frontend dependencies
cd ../frontend
npm install
```

### **Step 2: Start Services (In Separate Terminals)**

#### **Terminal 1: Backend**
```bash
cd backend
npm start
```

#### **Terminal 2: ML Service**
```bash
cd ml-service
python simple_ml_server.py
```

#### **Terminal 3: Frontend**
```bash
cd frontend
npm run dev
```

### **Step 3: Test Connection**
```bash
python test_connection.py
```

## 🌐 Access Your Application

- **Main App**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **ML Service**: http://localhost:5001
- **Analytics**: http://localhost:5002

## 🔧 Troubleshooting

### **Python 3.12 Issues**
If you get `distutils` errors:
```bash
# Use the simple ML service instead
cd ml-service
python simple_ml_server.py
```

### **Port Conflicts**
```bash
# Kill processes using ports
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :5001
taskkill /PID <PID> /F
```

### **Missing Dependencies**
```bash
# Reinstall dependencies
npm cache clean --force
npm install
```

## ✅ Success Indicators

You'll know it's working when:
- ✅ All three services start without errors
- ✅ Browser opens to http://localhost:3000
- ✅ You can see the B2B marketplace interface
- ✅ AI recommendations work
- ✅ No connection errors in console

## 🎯 What You'll See

1. **Frontend**: Modern B2B marketplace with React
2. **Backend**: REST API serving data
3. **ML Service**: AI-powered product recommendations
4. **Integration**: All services communicating seamlessly

---

**Ready to build your B2B marketplace! 🚀**
