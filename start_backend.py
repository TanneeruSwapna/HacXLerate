#!/usr/bin/env python3
"""
Backend startup script for the B2B Marketplace
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_node_npm():
    """Check if Node.js and npm are installed"""
    try:
        # Check Node.js
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("❌ Node.js not found. Please install Node.js")
            return False
        logger.info(f"✅ Node.js: {result.stdout.strip()}")
        
        # Check npm
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("❌ npm not found")
            return False
        logger.info(f"✅ npm: {result.stdout.strip()}")
        
        return True
    except FileNotFoundError:
        logger.error("❌ Node.js or npm not found. Please install them")
        return False

def install_dependencies():
    """Install backend dependencies"""
    logger.info("📦 Installing backend dependencies...")
    try:
        result = subprocess.run(
            ['npm', 'install'],
            cwd='backend',
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            logger.info("✅ Dependencies installed successfully")
            return True
        else:
            logger.error(f"❌ Dependency installation failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Dependency installation timed out")
        return False
    except Exception as e:
        logger.error(f"❌ Error installing dependencies: {e}")
        return False

def start_backend():
    """Start the backend server"""
    logger.info("🚀 Starting Backend Server...")
    try:
        process = subprocess.Popen(
            ['npm', 'start'],
            cwd='backend'
        )
        
        logger.info("✅ Backend server started on http://localhost:5000")
        logger.info("🛑 Press Ctrl+C to stop")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("🛑 Stopping backend server...")
        process.terminate()
        process.wait()
        logger.info("✅ Backend server stopped")
    except Exception as e:
        logger.error(f"❌ Error starting backend: {e}")

def main():
    """Main function"""
    logger.info("🚀 Starting B2B Marketplace Backend...")
    
    # Check prerequisites
    if not check_node_npm():
        sys.exit(1)
    
    # Check if backend directory exists
    if not Path('backend').exists():
        logger.error("❌ Backend directory not found")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
