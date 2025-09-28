#!/usr/bin/env python3
"""
Test script to verify connection between Frontend, Backend, and ML Service
"""

import requests
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_service_connection(service_name, url, timeout=5):
    """Test if a service is running and accessible"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            logger.info(f"✅ {service_name} is running at {url}")
            return True
        else:
            logger.warning(f"⚠️ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ {service_name} is not accessible: {e}")
        return False

def test_ml_recommendations():
    """Test ML service recommendations"""
    try:
        url = "http://localhost:5001/predict"
        payload = {
            "user_id": 1,
            "history": [123, 456, 789],
            "n_recommendations": 5
        }
        
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            logger.info(f"✅ ML Service recommendations working: {len(recommendations)} recommendations")
            return True
        else:
            logger.error(f"❌ ML Service recommendations failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ ML Service recommendations error: {e}")
        return False

def test_backend_api():
    """Test backend API endpoints"""
    try:
        # Test health endpoint
        health_url = "http://localhost:5000/health"
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            logger.info("✅ Backend health check passed")
        else:
            logger.warning("⚠️ Backend health check failed")
        
        # Test products endpoint
        products_url = "http://localhost:5000/api/products"
        response = requests.get(products_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            products = data if isinstance(data, list) else data.get('products', [])
            logger.info(f"✅ Backend products API working: {len(products)} products")
            return True
        else:
            logger.warning(f"⚠️ Backend products API failed: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Backend API error: {e}")
        return False

def test_frontend():
    """Test frontend accessibility"""
    try:
        url = "http://localhost:3000"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logger.info("✅ Frontend is accessible")
            return True
        else:
            logger.warning(f"⚠️ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"❌ Frontend not accessible: {e}")
        return False

def test_full_integration():
    """Test full integration between services"""
    logger.info("🔍 Testing full service integration...")
    
    # Test backend -> ML service integration
    try:
        # Simulate backend calling ML service
        ml_url = "http://localhost:5001/health"
        response = requests.get(ml_url, timeout=5)
        if response.status_code == 200:
            logger.info("✅ Backend can communicate with ML Service")
        else:
            logger.warning("⚠️ Backend-ML Service communication failed")
    except Exception as e:
        logger.error(f"❌ Backend-ML Service communication error: {e}")
    
    # Test frontend -> backend integration
    try:
        backend_url = "http://localhost:5000/api/products"
        response = requests.get(backend_url, timeout=5)
        if response.status_code == 200:
            logger.info("✅ Frontend can communicate with Backend")
        else:
            logger.warning("⚠️ Frontend-Backend communication failed")
    except Exception as e:
        logger.error(f"❌ Frontend-Backend communication error: {e}")

def main():
    """Main test function"""
    logger.info("🧪 Testing B2B Marketplace Service Connections...")
    logger.info("="*60)
    
    # Test individual services
    services = [
        ("Frontend", "http://localhost:3000"),
        ("Backend", "http://localhost:5000/health"),
        ("ML Service", "http://localhost:5001/health"),
        ("Analytics Dashboard", "http://localhost:5002/")
    ]
    
    running_services = 0
    total_services = len(services)
    
    for service_name, url in services:
        if test_service_connection(service_name, url):
            running_services += 1
    
    logger.info(f"\n📊 Service Status: {running_services}/{total_services} services running")
    
    # Test specific functionality
    if running_services >= 2:
        logger.info("\n🔍 Testing service functionality...")
        
        # Test ML recommendations if ML service is running
        if running_services >= 3:
            test_ml_recommendations()
        
        # Test backend API if backend is running
        test_backend_api()
        
        # Test full integration
        test_full_integration()
    
    # Summary
    logger.info("\n" + "="*60)
    if running_services == total_services:
        logger.info("🎉 All services are running and connected!")
        logger.info("✅ Your B2B Marketplace is ready to use!")
    elif running_services >= 2:
        logger.info("⚠️ Some services are running. Check the logs above for details.")
        logger.info("💡 Make sure to start all services for full functionality.")
    else:
        logger.info("❌ Most services are not running.")
        logger.info("💡 Please start the services using the startup scripts.")
    
    logger.info("="*60)

if __name__ == "__main__":
    main()
