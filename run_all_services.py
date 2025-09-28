#!/usr/bin/env python3
"""
Master startup script for the complete B2B Marketplace application
This script starts all services: Frontend, Backend, and ML Service
"""

import subprocess
import time
import sys
import os
import signal
import logging
import threading
from pathlib import Path
import webbrowser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class B2BMarketplaceManager:
    def __init__(self):
        self.processes = {}
        self.base_dir = Path(__file__).parent
        self.services_status = {}
        
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        logger.info("🔍 Checking dependencies for all services...")
        
        # Check Node.js for frontend
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ Node.js: {result.stdout.strip()}")
            else:
                logger.error("❌ Node.js not found. Please install Node.js")
                return False
        except FileNotFoundError:
            logger.error("❌ Node.js not found. Please install Node.js")
            return False
        
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ npm: {result.stdout.strip()}")
            else:
                logger.error("❌ npm not found")
                return False
        except FileNotFoundError:
            logger.error("❌ npm not found")
            return False
        
        # Check Python
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ is required")
            return False
        logger.info(f"✅ Python: {sys.version}")
        
        # Check if directories exist
        required_dirs = ['frontend', 'backend', 'ml-service']
        for dir_name in required_dirs:
            if not (self.base_dir / dir_name).exists():
                logger.error(f"❌ {dir_name} directory not found")
                return False
            logger.info(f"✅ {dir_name} directory exists")
        
        return True
    
    def install_frontend_dependencies(self):
        """Install frontend dependencies"""
        logger.info("📦 Installing frontend dependencies...")
        try:
            frontend_dir = self.base_dir / "frontend"
            result = subprocess.run(
                ['npm', 'install'],
                cwd=frontend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            if result.returncode == 0:
                logger.info("✅ Frontend dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ Frontend dependency installation failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("❌ Frontend dependency installation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Frontend dependency installation error: {e}")
            return False
    
    def install_backend_dependencies(self):
        """Install backend dependencies"""
        logger.info("📦 Installing backend dependencies...")
        try:
            backend_dir = self.base_dir / "backend"
            result = subprocess.run(
                ['npm', 'install'],
                cwd=backend_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            if result.returncode == 0:
                logger.info("✅ Backend dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ Backend dependency installation failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("❌ Backend dependency installation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Backend dependency installation error: {e}")
            return False
    
    def install_ml_dependencies(self):
        """Install ML service dependencies"""
        logger.info("📦 Installing ML service dependencies...")
        try:
            ml_dir = self.base_dir / "ml-service"
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                cwd=ml_dir,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout
            )
            if result.returncode == 0:
                logger.info("✅ ML service dependencies installed successfully")
                return True
            else:
                logger.error(f"❌ ML service dependency installation failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            logger.error("❌ ML service dependency installation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ ML service dependency installation error: {e}")
            return False
    
    def start_backend(self):
        """Start the backend service"""
        logger.info("🚀 Starting Backend Service...")
        try:
            backend_dir = self.base_dir / "backend"
            process = subprocess.Popen(
                ['npm', 'start'],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['backend'] = process
            self.services_status['backend'] = 'starting'
            
            # Wait a bit and check if it's running
            time.sleep(5)
            if process.poll() is None:
                logger.info("✅ Backend service started on port 5000")
                self.services_status['backend'] = 'running'
                return True
            else:
                logger.error("❌ Backend service failed to start")
                self.services_status['backend'] = 'failed'
                return False
        except Exception as e:
            logger.error(f"❌ Failed to start backend service: {e}")
            self.services_status['backend'] = 'error'
            return False
    
    def start_ml_service(self):
        """Start the ML service"""
        logger.info("🤖 Starting ML Service...")
        try:
            ml_dir = self.base_dir / "ml-service"
            
            # Generate data if it doesn't exist
            data_dir = ml_dir / "data"
            if not data_dir.exists():
                logger.info("📊 Generating sample data for ML service...")
                subprocess.run([sys.executable, 'enhanced_data_generator.py'], 
                             cwd=ml_dir, timeout=300)
            
            # Start ML service
            process = subprocess.Popen(
                [sys.executable, 'advanced_ml_server.py'],
                cwd=ml_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['ml_service'] = process
            self.services_status['ml_service'] = 'starting'
            
            # Wait a bit and check if it's running
            time.sleep(8)
            if process.poll() is None:
                logger.info("✅ ML service started on port 5001")
                self.services_status['ml_service'] = 'running'
                
                # Train models in background
                threading.Thread(target=self.train_ml_models, daemon=True).start()
                return True
            else:
                logger.error("❌ ML service failed to start")
                self.services_status['ml_service'] = 'failed'
                return False
        except Exception as e:
            logger.error(f"❌ Failed to start ML service: {e}")
            self.services_status['ml_service'] = 'error'
            return False
    
    def train_ml_models(self):
        """Train ML models in background"""
        try:
            logger.info("🧠 Training ML models...")
            import requests
            time.sleep(10)  # Give ML service time to fully start
            
            response = requests.post("http://localhost:5001/train", timeout=300)
            if response.status_code == 200:
                logger.info("✅ ML models trained successfully")
                self.services_status['ml_service'] = 'ready'
            else:
                logger.warning("⚠️ ML model training failed, but service is running")
        except Exception as e:
            logger.warning(f"⚠️ ML model training error: {e}")
    
    def start_frontend(self):
        """Start the frontend service"""
        logger.info("🎨 Starting Frontend Service...")
        try:
            frontend_dir = self.base_dir / "frontend"
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['frontend'] = process
            self.services_status['frontend'] = 'starting'
            
            # Wait a bit and check if it's running
            time.sleep(8)
            if process.poll() is None:
                logger.info("✅ Frontend service started on port 3000")
                self.services_status['frontend'] = 'running'
                return True
            else:
                logger.error("❌ Frontend service failed to start")
                self.services_status['frontend'] = 'failed'
                return False
        except Exception as e:
            logger.error(f"❌ Failed to start frontend service: {e}")
            self.services_status['frontend'] = 'error'
            return False
    
    def start_analytics_dashboard(self):
        """Start the analytics dashboard"""
        logger.info("📊 Starting Analytics Dashboard...")
        try:
            ml_dir = self.base_dir / "ml-service"
            process = subprocess.Popen(
                [sys.executable, 'analytics_dashboard.py'],
                cwd=ml_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes['analytics'] = process
            self.services_status['analytics'] = 'starting'
            
            # Wait a bit and check if it's running
            time.sleep(5)
            if process.poll() is None:
                logger.info("✅ Analytics dashboard started on port 5002")
                self.services_status['analytics'] = 'running'
                return True
            else:
                logger.error("❌ Analytics dashboard failed to start")
                self.services_status['analytics'] = 'failed'
                return False
        except Exception as e:
            logger.error(f"❌ Failed to start analytics dashboard: {e}")
            self.services_status['analytics'] = 'error'
            return False
    
    def check_service_health(self):
        """Check health of all services"""
        logger.info("🏥 Checking service health...")
        
        import requests
        
        services = [
            ('Backend', 'http://localhost:5000/health'),
            ('ML Service', 'http://localhost:5001/health'),
            ('Analytics', 'http://localhost:5002/')
        ]
        
        for name, url in services:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    logger.info(f"✅ {name} is healthy")
                else:
                    logger.warning(f"⚠️ {name} returned status {response.status_code}")
            except Exception as e:
                logger.warning(f"⚠️ {name} health check failed: {e}")
    
    def print_service_info(self):
        """Print information about all running services"""
        print("\n" + "="*70)
        print("🎉 B2B Marketplace Application Started Successfully!")
        print("="*70)
        print("\n📱 Available Services:")
        print("  • Frontend (React):     http://localhost:3000")
        print("  • Backend (Node.js):    http://localhost:5000")
        print("  • ML Service:           http://localhost:5001")
        print("  • Analytics Dashboard:  http://localhost:5002")
        
        print("\n🔗 Key Endpoints:")
        print("  • Main Application:     http://localhost:3000")
        print("  • API Health:           http://localhost:5000/health")
        print("  • ML Health:            http://localhost:5001/health")
        print("  • Analytics:            http://localhost:5002/")
        
        print("\n📚 API Examples:")
        print("  • Get Products:         GET http://localhost:5000/api/products")
        print("  • Get Recommendations:  POST http://localhost:5000/api/recommendations")
        print("  • Train ML Models:      POST http://localhost:5001/train")
        
        print("\n🎯 Service Status:")
        for service, status in self.services_status.items():
            status_emoji = "✅" if status == "running" else "🔄" if status == "starting" else "❌"
            print(f"  {status_emoji} {service.title()}: {status}")
        
        print("\n🛑 To stop all services: Ctrl+C")
        print("="*70)
        
        # Open browser to main application
        try:
            webbrowser.open('http://localhost:3000')
            logger.info("🌐 Opened browser to main application")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")
    
    def stop_all_services(self):
        """Stop all running services"""
        logger.info("🛑 Stopping all services...")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"✅ {name} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.info(f"✅ {name} force stopped")
            except Exception as e:
                logger.error(f"❌ Error stopping {name}: {e}")
        
        self.processes.clear()
        self.services_status.clear()
        logger.info("🛑 All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"📡 Received signal {signum}, shutting down...")
        self.stop_all_services()
        sys.exit(0)
    
    def run_all_services(self, install_deps=False, open_browser=True):
        """Run all services"""
        logger.info("🚀 Starting B2B Marketplace Application...")
        
        # Check dependencies
        if not self.check_dependencies():
            logger.error("❌ Dependency check failed. Exiting.")
            return False
        
        # Install dependencies if requested
        if install_deps:
            logger.info("📦 Installing dependencies...")
            if not self.install_frontend_dependencies():
                return False
            if not self.install_backend_dependencies():
                return False
            if not self.install_ml_dependencies():
                return False
        
        # Start services in order
        logger.info("🚀 Starting services...")
        
        # 1. Start Backend first
        if not self.start_backend():
            logger.error("❌ Failed to start backend. Exiting.")
            return False
        
        # 2. Start ML Service
        if not self.start_ml_service():
            logger.warning("⚠️ ML service failed to start, but continuing...")
        
        # 3. Start Analytics Dashboard
        self.start_analytics_dashboard()  # Optional service
        
        # 4. Start Frontend last
        if not self.start_frontend():
            logger.error("❌ Failed to start frontend. Exiting.")
            return False
        
        # Wait for all services to stabilize
        time.sleep(5)
        
        # Check health
        self.check_service_health()
        
        # Print service information
        self.print_service_info()
        
        return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start B2B Marketplace Application")
    parser.add_argument("--install", action="store_true", help="Install dependencies before starting")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    args = parser.parse_args()
    
    manager = B2BMarketplaceManager()
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    try:
        # Start all services
        if manager.run_all_services(install_deps=args.install, open_browser=not args.no_browser):
            logger.info("🎉 All services started successfully!")
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("📡 Received keyboard interrupt")
        else:
            logger.error("❌ Failed to start services")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        manager.stop_all_services()
        sys.exit(1)
    
    finally:
        manager.stop_all_services()

if __name__ == "__main__":
    main()
