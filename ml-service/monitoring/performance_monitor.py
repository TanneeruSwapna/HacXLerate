"""
Performance monitoring utilities
"""

import time
import psutil
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor model and system performance"""
    
    def __init__(self):
        self.metrics_history = []
        self.start_time = time.time()
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'uptime': time.time() - self.start_time
        }
    
    def get_model_metrics(self, model_name: str, 
                         inference_time: float, 
                         recommendations_count: int) -> Dict[str, Any]:
        """Get model performance metrics"""
        return {
            'model_name': model_name,
            'inference_time': inference_time,
            'recommendations_per_second': recommendations_count / inference_time if inference_time > 0 else 0,
            'timestamp': time.time()
        }
    
    def log_metrics(self, metrics: Dict[str, Any]):
        """Log performance metrics"""
        self.metrics_history.append(metrics)
        
        # Keep only last 1000 entries
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {}
        
        # Calculate averages
        avg_inference_time = sum(m.get('inference_time', 0) for m in self.metrics_history) / len(self.metrics_history)
        avg_recommendations_per_second = sum(m.get('recommendations_per_second', 0) for m in self.metrics_history) / len(self.metrics_history)
        
        return {
            'total_requests': len(self.metrics_history),
            'avg_inference_time': avg_inference_time,
            'avg_recommendations_per_second': avg_recommendations_per_second,
            'system_metrics': self.get_system_metrics()
        }
