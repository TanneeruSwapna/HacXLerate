# 🚀 How to Run the B2B Marketplace Application

## 🎯 Quick Start (Easiest Method)

### **Windows Users**
```bash
# Double-click or run:
start_all.bat
```

### **Linux/Mac Users**
```bash
# Make executable and run:
chmod +x start_all.sh
./start_all.sh
```

### **Universal Method (All Platforms)**
```bash
# Install dependencies and start all services
python run_all_services.py --install
```

## 📋 What This Does

The startup script will automatically:
1. ✅ Check if Node.js and Python are installed
2. 📦 Install all dependencies (npm packages, Python packages)
3. 🚀 Start all services in the correct order:
   - Backend (Node.js) on port 5000
   - ML Service (Python) on port 5001
   - Frontend (React) on port 3000
   - Analytics Dashboard on port 5002
4. 🌐 Open your browser to the application
5. 📊 Show service status and URLs

## 🌐 Access Your Application

Once started, you can access:

| Service | URL | What You'll See |
|---------|-----|----------------|
| **Main App** | http://localhost:3000 | B2B Marketplace Interface |
| **API** | http://localhost:5000 | Backend API Endpoints |
| **ML Service** | http://localhost:5001 | AI Recommendation Service |
| **Analytics** | http://localhost:5002 | ML Performance Dashboard |

## 🔧 Manual Setup (If Needed)

### **Step 1: Backend**
```bash
cd backend
npm install
npm start
```

### **Step 2: ML Service**
```bash
cd ml-service
pip install -r requirements.txt
python enhanced_data_generator.py
python advanced_ml_server.py
```

### **Step 3: Frontend**
```bash
cd frontend
npm install
npm run dev
```

## 🛠 Prerequisites

Make sure you have installed:
- **Node.js** (v16+) - [Download](https://nodejs.org/)
- **Python** (3.8+) - [Download](https://python.org/)

## 🆘 Troubleshooting

### **Port Already in Use**
```bash
# Find what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Kill the process (Windows)
taskkill /PID <PID> /F
```

### **Dependencies Issues**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall Python packages
pip install -r ml-service/requirements.txt --force-reinstall
```

### **Service Won't Start**
1. Check if all prerequisites are installed
2. Make sure ports 3000, 5000, 5001 are free
3. Check the terminal for error messages
4. Try starting services individually

## 📞 Need Help?

1. Check the detailed `STARTUP_GUIDE.md`
2. Look at error messages in the terminal
3. Verify all services are running by visiting the URLs above
4. Make sure MongoDB is running (if using local database)

## 🎉 Success!

When everything is working, you'll see:
- ✅ All services running without errors
- 🌐 Browser opens to http://localhost:3000
- 📊 B2B marketplace interface loads
- 🤖 AI recommendations working
- 📈 Analytics dashboard accessible

**Enjoy your B2B Marketplace with AI-powered recommendations! 🚀**
