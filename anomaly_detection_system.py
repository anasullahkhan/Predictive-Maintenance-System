import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# PREDICTIVE MAINTENANCE SYSTEM
# Complete Equipment Anomaly Detection & Failure Prediction

class PredictiveMaintenanceSystem:
    """Equipment monitoring for anomaly detection & failure prediction"""
    
    def __init__(self):
        print("PREDICTIVE MAINTENANCE SYSTEM INITIALIZED")
    
    def train(self, sensor_vib, sensor_temp, sensor_curr):
        """Learn normal equipment behavior"""
        self.vib_mean = np.mean(sensor_vib)
        self.vib_std = np.std(sensor_vib)
        self.temp_mean = np.mean(sensor_temp)
        self.temp_std = np.std(sensor_temp)
        self.curr_mean = np.mean(sensor_curr)
        self.curr_std = np.std(sensor_curr)
        
        self.vib_critical = self.vib_mean + 4.5 * self.vib_std
        self.temp_critical = self.temp_mean + 8 * self.temp_std
        self.curr_critical = self.curr_mean + 5 * self.curr_std
        
        print("✅ System trained on normal data")
    
    def predict(self, curr_vib, curr_temp, curr_curr, trend_vib, trend_temp, trend_curr):
        """Predict equipment failure"""
        
        time_vib = self._calc_time_to_failure(curr_vib, trend_vib, self.vib_critical)
        time_temp = self._calc_time_to_failure(curr_temp, trend_temp, self.temp_critical)
        time_curr = self._calc_time_to_failure(curr_curr, trend_curr, self.curr_critical)
        
        times = [t for t in [time_vib, time_temp, time_curr] if t is not None]
        overall_time = min(times) if times else None
        
        return {
            'failure_days': overall_time,
            'severity': self._get_severity(overall_time),
            'recommendation': self._get_recommendation(overall_time)
        }
    
    def _calc_time_to_failure(self, current, trend, threshold):
        if trend <= 0:
            return None
        distance = threshold - current
        if distance <= 0:
            return 0
        return max(0, distance / trend / 100)
    
    def _get_severity(self, days):
        if days is None or days > 30:
            return "LOW 🟢"
        elif days > 7:
            return "MEDIUM 🟡"
        elif days > 1:
            return "HIGH ⚠️"
        else:
            return "CRITICAL 🔴"
    
    def _get_recommendation(self, days):
        if days is None or days > 30:
            return "Monitor equipment. Schedule maintenance within month."
        elif days > 7:
            return "Schedule maintenance THIS WEEK"
        elif days > 1:
            return "Schedule maintenance WITHIN 24-48 HOURS"
        else:
            return "STOP EQUIPMENT IMMEDIATELY!"

if __name__ == "__main__":
    print("Predictive Maintenance System Ready")
