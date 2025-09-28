"""
Alert system for monitoring
"""

import logging
from typing import Dict, Any, List, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertSystem:
    """Alert system for monitoring"""
    
    def __init__(self):
        self.alerts = []
        self.alert_handlers = []
    
    def add_alert_handler(self, handler: Callable[[Dict[str, Any]], None]):
        """Add alert handler"""
        self.alert_handlers.append(handler)
    
    def check_performance_alerts(self, metrics: Dict[str, Any]):
        """Check performance-based alerts"""
        # High inference time alert
        if metrics.get('inference_time', 0) > 1.0:  # 1 second
            self._trigger_alert({
                'type': 'high_inference_time',
                'message': f"High inference time: {metrics['inference_time']:.3f}s",
                'severity': 'warning',
                'timestamp': datetime.now().isoformat()
            })
        
        # Low throughput alert
        if metrics.get('recommendations_per_second', 0) < 10:
            self._trigger_alert({
                'type': 'low_throughput',
                'message': f"Low throughput: {metrics['recommendations_per_second']:.1f} rec/s",
                'severity': 'warning',
                'timestamp': datetime.now().isoformat()
            })
    
    def check_system_alerts(self, system_metrics: Dict[str, Any]):
        """Check system-based alerts"""
        # High CPU usage
        if system_metrics.get('cpu_percent', 0) > 80:
            self._trigger_alert({
                'type': 'high_cpu',
                'message': f"High CPU usage: {system_metrics['cpu_percent']:.1f}%",
                'severity': 'warning',
                'timestamp': datetime.now().isoformat()
            })
        
        # High memory usage
        if system_metrics.get('memory_percent', 0) > 85:
            self._trigger_alert({
                'type': 'high_memory',
                'message': f"High memory usage: {system_metrics['memory_percent']:.1f}%",
                'severity': 'critical',
                'timestamp': datetime.now().isoformat()
            })
    
    def check_drift_alerts(self, drift_results: Dict[str, Any]):
        """Check data drift alerts"""
        for drift_type, drift_data in drift_results.items():
            if drift_data.get('drift_detected', False):
                self._trigger_alert({
                    'type': f'data_drift_{drift_type}',
                    'message': f"Data drift detected in {drift_type}",
                    'severity': 'warning',
                    'timestamp': datetime.now().isoformat(),
                    'details': drift_data
                })
    
    def _trigger_alert(self, alert: Dict[str, Any]):
        """Trigger an alert"""
        self.alerts.append(alert)
        
        # Log the alert
        logger.warning(f"ALERT: {alert['message']}")
        
        # Send to handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Alert handler error: {e}")
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        return self.alerts[-limit:] if self.alerts else []
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        logger.info("All alerts cleared")
