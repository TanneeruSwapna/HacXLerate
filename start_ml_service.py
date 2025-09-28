#!/usr/bin/env python3
"""
ML Service startup script for the B2B Marketplace
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python():
    """Check Python version"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ is required")
        return False
    logger.info(f"✅ Python: {sys.version}")
    return True

def install_dependencies():
    """Install ML service dependencies"""
    logger.info("📦 Installing ML service dependencies...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'minimal_requirements.txt'],
            cwd='ml-service',
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
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

def generate_sample_data():
    """Generate sample data if it doesn't exist"""
    data_dir = Path('ml-service/data')
    if not data_dir.exists():
        logger.info("📊 Generating sample data...")
        try:
            result = subprocess.run(
                [sys.executable, 'enhanced_data_generator.py'],
                cwd='ml-service',
                timeout=300
            )
            if result.returncode == 0:
                logger.info("✅ Sample data generated successfully")
                return True
            else:
                logger.error("❌ Failed to generate sample data")
                return False
        except subprocess.TimeoutExpired:
            logger.error("❌ Data generation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error generating data: {e}")
            return False
    else:
        logger.info("✅ Sample data already exists")
        return True

def start_simple_ml_service():
    """Start the simple ML service"""
    logger.info("🤖 Starting Simple ML Service...")
    try:
        process = subprocess.Popen(
            [sys.executable, 'simple_ml_server.py'],
            cwd='ml-service'
        )
        
        logger.info("✅ Simple ML service started on http://localhost:5001")
        logger.info("🛑 Press Ctrl+C to stop")
        
        # Wait for the process
        process.wait()
        
    except KeyboardInterrupt:
        logger.info("🛑 Stopping ML service...")
        process.terminate()
        process.wait()
        logger.info("✅ ML service stopped")
    except Exception as e:
        logger.error(f"❌ Error starting ML service: {e}")

def main():
    """Main function"""
    logger.info("🚀 Starting B2B Marketplace ML Service...")
    
    # Check prerequisites
    if not check_python():
        sys.exit(1)
    
    # Check if ml-service directory exists
    if not Path('ml-service').exists():
        logger.error("❌ ML service directory not found")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Generate sample data
    if not generate_sample_data():
        sys.exit(1)
    
    # Start ML service (using simple version for compatibility)
    start_simple_ml_service()

if __name__ == "__main__":
    main()
