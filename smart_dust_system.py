"""
Smart Dust Technology Simulation System
Simulates environmental dust detection using virtual Smart Dust motes
"""

import random
import time
import threading
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict
from collections import deque
import json


@dataclass
class DustReading:
    """Represents a single dust/pollution reading from a mote"""
    mote_id: str
    timestamp: datetime
    pm25: float  # PM2.5 particles (ug/m3)
    pm10: float  # PM10 particles (ug/m3)
    temperature: float  # Temperature in Celsius
    humidity: float  # Humidity percentage
    location: tuple  # (x, y) coordinates


class SmartDustMote:
    """Simulates a single Smart Dust mote (sensor node)"""
    
    # Safe thresholds (WHO guidelines)
    PM25_SAFE_THRESHOLD = 25.0  # ug/m3
    PM10_SAFE_THRESHOLD = 50.0  # ug/m3
    
    def __init__(self, mote_id: str, location: tuple, base_pollution: float = 0.0):
        """
        Initialize a Smart Dust mote
        
        Args:
            mote_id: Unique identifier for the mote
            location: (x, y) coordinates of the mote
            base_pollution: Base pollution level (0.0 to 1.0)
        """
        self.mote_id = mote_id
        self.location = location
        self.base_pollution = base_pollution
        self.is_active = True
        self.reading_history = deque(maxlen=100)  # Store last 100 readings
        
    def sense(self) -> DustReading:
        """
        Generate a dust reading with realistic variations
        
        Returns:
            DustReading object with sensor data
        """
        # Simulate realistic dust levels with some randomness
        # Higher base_pollution leads to higher readings
        pm25_base = 10.0 + (self.base_pollution * 40.0)
        pm10_base = 20.0 + (self.base_pollution * 60.0)
        
        # Add realistic variations (simulating wind, time of day, etc.)
        time_factor = 1.0 + 0.3 * random.gauss(0, 1)  # Random variation
        pm25 = max(0, pm25_base * time_factor + random.gauss(0, 5))
        pm10 = max(0, pm10_base * time_factor + random.gauss(0, 8))
        
        # Simulate environmental conditions
        temperature = 20.0 + random.gauss(0, 5)  # Room temperature with variation
        humidity = 40.0 + random.gauss(0, 15)  # Humidity with variation
        humidity = max(0, min(100, humidity))  # Clamp to 0-100
        
        reading = DustReading(
            mote_id=self.mote_id,
            timestamp=datetime.now(),
            pm25=round(pm25, 2),
            pm10=round(pm10, 2),
            temperature=round(temperature, 2),
            humidity=round(humidity, 2),
            location=self.location
        )
        
        self.reading_history.append(reading)
        return reading
    
    def get_average_pollution(self) -> Dict[str, float]:
        """Calculate average pollution levels from recent readings"""
        if not self.reading_history:
            return {"pm25": 0.0, "pm10": 0.0}
        
        avg_pm25 = sum(r.pm25 for r in self.reading_history) / len(self.reading_history)
        avg_pm10 = sum(r.pm10 for r in self.reading_history) / len(self.reading_history)
        
        return {
            "pm25": round(avg_pm25, 2),
            "pm10": round(avg_pm10, 2)
        }
    
    def is_pollution_unsafe(self, reading: DustReading) -> bool:
        """Check if pollution levels exceed safe thresholds"""
        return (reading.pm25 > self.PM25_SAFE_THRESHOLD or 
                reading.pm10 > self.PM10_SAFE_THRESHOLD)


class DataProcessor:
    """Processes and analyzes dust data from multiple motes"""
    
    def __init__(self):
        self.all_readings: List[DustReading] = []
        self.alert_history: List[Dict] = []
    
    def add_reading(self, reading: DustReading):
        """Add a new reading to the processor"""
        self.all_readings.append(reading)
        # Keep only last 1000 readings to manage memory
        if len(self.all_readings) > 1000:
            self.all_readings = self.all_readings[-1000:]
    
    def analyze_reading(self, reading: DustReading) -> Dict:
        """
        Analyze a reading and determine pollution status
        
        Returns:
            Dictionary with analysis results
        """
        status = "SAFE"
        severity = "LOW"
        
        if reading.pm25 > SmartDustMote.PM25_SAFE_THRESHOLD:
            status = "UNSAFE"
            if reading.pm25 > 50:
                severity = "CRITICAL"
            elif reading.pm25 > 35:
                severity = "HIGH"
            else:
                severity = "MODERATE"
        
        if reading.pm10 > SmartDustMote.PM10_SAFE_THRESHOLD:
            status = "UNSAFE"
            if reading.pm10 > 100:
                severity = "CRITICAL"
            elif reading.pm10 > 70:
                severity = "HIGH"
            else:
                severity = "MODERATE"
        
        return {
            "status": status,
            "severity": severity,
            "pm25_level": reading.pm25,
            "pm10_level": reading.pm10,
            "pm25_threshold": SmartDustMote.PM25_SAFE_THRESHOLD,
            "pm10_threshold": SmartDustMote.PM10_SAFE_THRESHOLD
        }
    
    def get_statistics(self) -> Dict:
        """Calculate overall statistics from all readings"""
        if not self.all_readings:
            return {}
        
        recent_readings = self.all_readings[-100:]  # Last 100 readings
        
        pm25_values = [r.pm25 for r in recent_readings]
        pm10_values = [r.pm10 for r in recent_readings]
        
        return {
            "total_readings": len(self.all_readings),
            "recent_readings": len(recent_readings),
            "avg_pm25": round(sum(pm25_values) / len(pm25_values), 2),
            "avg_pm10": round(sum(pm10_values) / len(pm10_values), 2),
            "max_pm25": round(max(pm25_values), 2),
            "max_pm10": round(max(pm10_values), 2),
            "min_pm25": round(min(pm25_values), 2),
            "min_pm10": round(min(pm10_values), 2),
        }
    
    def get_pollution_map(self, motes: List[SmartDustMote]) -> Dict:
        """Create a pollution map from all active motes"""
        pollution_map = {}
        for mote in motes:
            if mote.is_active:
                avg = mote.get_average_pollution()
                pollution_map[mote.mote_id] = {
                    "location": mote.location,
                    "pm25": avg["pm25"],
                    "pm10": avg["pm10"],
                    "status": "UNSAFE" if (avg["pm25"] > SmartDustMote.PM25_SAFE_THRESHOLD or 
                                          avg["pm10"] > SmartDustMote.PM10_SAFE_THRESHOLD) else "SAFE"
                }
        return pollution_map


class AlertSystem:
    """Generates and manages pollution alerts"""
    
    def __init__(self):
        self.alerts: List[Dict] = []
        self.alert_callbacks = []
    
    def check_and_alert(self, reading: DustReading, analysis: Dict):
        """
        Check if alert should be generated and create it
        
        Args:
            reading: The dust reading
            analysis: Analysis results from DataProcessor
        """
        if analysis["status"] == "UNSAFE":
            alert = {
                "timestamp": reading.timestamp.isoformat(),
                "mote_id": reading.mote_id,
                "location": reading.location,
                "severity": analysis["severity"],
                "pm25": reading.pm25,
                "pm10": reading.pm10,
                "message": self._generate_alert_message(reading, analysis)
            }
            
            self.alerts.append(alert)
            # Keep only last 100 alerts
            if len(self.alerts) > 100:
                self.alerts = self.alerts[-100:]
            
            # Trigger callbacks
            for callback in self.alert_callbacks:
                callback(alert)
    
    def _generate_alert_message(self, reading: DustReading, analysis: Dict) -> str:
        """Generate human-readable alert message"""
        issues = []
        if reading.pm25 > SmartDustMote.PM25_SAFE_THRESHOLD:
            issues.append(f"PM2.5: {reading.pm25} ug/m3 (threshold: {SmartDustMote.PM25_SAFE_THRESHOLD})")
        if reading.pm10 > SmartDustMote.PM10_SAFE_THRESHOLD:
            issues.append(f"PM10: {reading.pm10} ug/m3 (threshold: {SmartDustMote.PM10_SAFE_THRESHOLD})")
        
        return f"[!] {analysis['severity']} ALERT at Mote {reading.mote_id}: " + ", ".join(issues)
    
    def get_recent_alerts(self, count: int = 10) -> List[Dict]:
        """Get the most recent alerts"""
        return self.alerts[-count:] if self.alerts else []
    
    def register_callback(self, callback):
        """Register a callback function to be called when alerts are generated"""
        self.alert_callbacks.append(callback)


class SmartDustSimulation:
    """Main simulation system that orchestrates all components"""
    
    def __init__(self, num_motes: int = 5):
        """
        Initialize the Smart Dust simulation
        
        Args:
            num_motes: Number of virtual motes to create
        """
        self.motes: List[SmartDustMote] = []
        self.processor = DataProcessor()
        self.alert_system = AlertSystem()
        self.is_running = False
        self.sampling_interval = 2.0  # seconds between readings
        
        # Create virtual motes with different pollution levels
        for i in range(num_motes):
            location = (random.uniform(0, 100), random.uniform(0, 100))
            base_pollution = random.uniform(0.0, 0.8)  # Varying pollution levels
            mote = SmartDustMote(f"MOTE-{i+1:03d}", location, base_pollution)
            self.motes.append(mote)
        
        # Register alert callback for console output
        self.alert_system.register_callback(self._on_alert)
    
    def _on_alert(self, alert: Dict):
        """Callback function when an alert is generated"""
        print(f"\n[ALERT] {alert['message']}")
        print(f"   Location: {alert['location']} | Time: {alert['timestamp']}\n")
    
    def start_simulation(self, duration: int = 60):
        """
        Start the simulation
        
        Args:
            duration: Duration in seconds to run the simulation
        """
        self.is_running = True
        print("=" * 60)
        print("SMART DUST SIMULATION SYSTEM STARTED")
        print("=" * 60)
        print(f"Active Motes: {len(self.motes)}")
        print(f"Sampling Interval: {self.sampling_interval} seconds")
        print(f"Duration: {duration} seconds")
        print("=" * 60)
        print("\nMonitoring dust levels...\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while self.is_running and (time.time() - start_time) < duration:
                iteration += 1
                
                # Collect readings from all motes
                for mote in self.motes:
                    if mote.is_active:
                        reading = mote.sense()
                        self.processor.add_reading(reading)
                        
                        # Analyze the reading
                        analysis = self.processor.analyze_reading(reading)
                        
                        # Check for alerts
                        self.alert_system.check_and_alert(reading, analysis)
                
                # Display periodic status
                if iteration % 5 == 0:  # Every 5 iterations
                    self._display_status()
                
                time.sleep(self.sampling_interval)
        
        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user.")
        
        finally:
            self.stop_simulation()
    
    def _display_status(self):
        """Display current system status"""
        stats = self.processor.get_statistics()
        recent_alerts = self.alert_system.get_recent_alerts(3)
        
        print(f"\n[STATUS] Update - {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Total Readings: {stats.get('total_readings', 0)}")
        print(f"   Average PM2.5: {stats.get('avg_pm25', 0)} ug/m3")
        print(f"   Average PM10: {stats.get('avg_pm10', 0)} ug/m3")
        print(f"   Max PM2.5: {stats.get('max_pm25', 0)} ug/m3")
        print(f"   Max PM10: {stats.get('max_pm10', 0)} ug/m3")
        
        if recent_alerts:
            print(f"   [!] Recent Alerts: {len(recent_alerts)}")
        else:
            print(f"   [OK] No recent alerts - All levels safe")
    
    def stop_simulation(self):
        """Stop the simulation and display final report"""
        self.is_running = False
        print("\n" + "=" * 60)
        print("[FINAL SIMULATION REPORT]")
        print("=" * 60)
        
        stats = self.processor.get_statistics()
        print(f"\nTotal Readings Collected: {stats.get('total_readings', 0)}")
        print(f"Average PM2.5: {stats.get('avg_pm25', 0)} ug/m3")
        print(f"Average PM10: {stats.get('avg_pm10', 0)} ug/m3")
        print(f"Peak PM2.5: {stats.get('max_pm25', 0)} ug/m3")
        print(f"Peak PM10: {stats.get('max_pm10', 0)} ug/m3")
        
        print(f"\nTotal Alerts Generated: {len(self.alert_system.alerts)}")
        if self.alert_system.alerts:
            print("\nRecent Alerts:")
            for alert in self.alert_system.get_recent_alerts(5):
                print(f"  • {alert['message']}")
        
        # Display pollution map
        print("\n[POLLUTION MAP]")
        pollution_map = self.processor.get_pollution_map(self.motes)
        for mote_id, data in pollution_map.items():
            status_icon = "[UNSAFE]" if data["status"] == "UNSAFE" else "[SAFE]"
            print(f"  {status_icon} {mote_id}: PM2.5={data['pm25']}, PM10={data['pm10']} at {data['location']}")
        
        print("\n" + "=" * 60)
        print("Simulation completed successfully!")
        print("=" * 60)
    
    def get_data_for_visualization(self) -> Dict:
        """Get formatted data for visualization"""
        stats = self.processor.get_statistics()
        pollution_map = self.processor.get_pollution_map(self.motes)
        
        return {
            "statistics": stats,
            "pollution_map": pollution_map,
            "recent_readings": [
                {
                    "mote_id": r.mote_id,
                    "timestamp": r.timestamp.isoformat(),
                    "pm25": r.pm25,
                    "pm10": r.pm10,
                    "location": r.location
                }
                for r in self.processor.all_readings[-50:]  # Last 50 readings
            ],
            "alerts": self.alert_system.get_recent_alerts(10)
        }


def main():
    """Main entry point for the simulation"""
    print("\n" + "=" * 60)
    print("SMART DUST TECHNOLOGY SIMULATION")
    print("=" * 60)
    print("\nThis system simulates Smart Dust motes for environmental")
    print("dust detection and pollution monitoring.\n")
    
    # Create simulation with 5 motes
    simulation = SmartDustSimulation(num_motes=5)
    
    # Run simulation for 60 seconds
    simulation.start_simulation(duration=60)
    
    # Optionally save data to JSON
    data = simulation.get_data_for_visualization()
    with open("dust_simulation_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\n[SAVED] Simulation data saved to 'dust_simulation_data.json'")


if __name__ == "__main__":
    main()

