"""
Visualization module for Smart Dust Simulation
Creates graphs and charts for dust detection data
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import json
import os
from smart_dust_system import SmartDustSimulation, SmartDustMote


class DustVisualizer:
    """Creates visualizations for dust detection data"""
    
    def __init__(self, simulation: SmartDustSimulation):
        self.simulation = simulation
        self.fig = None
        self.axes = None
    
    def plot_real_time(self, duration: int = 60, update_interval: int = 2):
        """
        Create real-time updating plots
        
        Args:
            duration: Duration to run visualization in seconds
            update_interval: Update interval in seconds
        """
        self.fig, self.axes = plt.subplots(2, 2, figsize=(14, 10))
        self.fig.suptitle('Smart Dust Technology - Real-Time Monitoring', fontsize=16, fontweight='bold')
        
        # Start simulation in background
        import threading
        sim_thread = threading.Thread(target=self.simulation.start_simulation, args=(duration,))
        sim_thread.daemon = True
        sim_thread.start()
        
        # Animate plots
        ani = animation.FuncAnimation(
            self.fig, 
            self._update_plots, 
            interval=update_interval * 1000,  # Convert to milliseconds
            blit=False
        )
        
        plt.tight_layout()
        plt.show()
    
    def _update_plots(self, frame):
        """Update all plots with latest data"""
        if not self.simulation.processor.all_readings:
            return
        
        # Clear axes
        for ax in self.axes.flat:
            ax.clear()
        
        recent_readings = self.simulation.processor.all_readings[-50:]
        
        # Plot 1: PM2.5 and PM10 over time
        ax1 = self.axes[0, 0]
        timestamps = [r.timestamp for r in recent_readings]
        pm25_values = [r.pm25 for r in recent_readings]
        pm10_values = [r.pm10 for r in recent_readings]
        
        ax1.plot(timestamps, pm25_values, 'b-', label='PM2.5', linewidth=2)
        ax1.plot(timestamps, pm10_values, 'r-', label='PM10', linewidth=2)
        ax1.axhline(y=SmartDustMote.PM25_SAFE_THRESHOLD, color='b', linestyle='--', alpha=0.5, label='PM2.5 Threshold')
        ax1.axhline(y=SmartDustMote.PM10_SAFE_THRESHOLD, color='r', linestyle='--', alpha=0.5, label='PM10 Threshold')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Particle Concentration (ug/m3)')
        ax1.set_title('Dust Levels Over Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Pollution map (scatter plot by location)
        ax2 = self.axes[0, 1]
        pollution_map = self.simulation.processor.get_pollution_map(self.simulation.motes)
        
        x_coords = []
        y_coords = []
        pm25_values_map = []
        colors = []
        
        for mote_id, data in pollution_map.items():
            x_coords.append(data['location'][0])
            y_coords.append(data['location'][1])
            pm25_values_map.append(data['pm25'])
            colors.append('red' if data['status'] == 'UNSAFE' else 'green')
        
        if x_coords:
            scatter = ax2.scatter(x_coords, y_coords, c=colors, s=[v*10 for v in pm25_values_map], 
                                 alpha=0.6, edgecolors='black', linewidths=1)
            for i, (mote_id, data) in enumerate(pollution_map.items()):
                ax2.annotate(mote_id, (x_coords[i], y_coords[i]), fontsize=8)
        
        ax2.set_xlabel('X Coordinate')
        ax2.set_ylabel('Y Coordinate')
        ax2.set_title('Pollution Map (Size = PM2.5 Level)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Statistics bar chart
        ax3 = self.axes[1, 0]
        stats = self.simulation.processor.get_statistics()
        
        if stats:
            categories = ['Avg PM2.5', 'Avg PM10', 'Max PM2.5', 'Max PM10']
            values = [
                stats.get('avg_pm25', 0),
                stats.get('avg_pm10', 0),
                stats.get('max_pm25', 0),
                stats.get('max_pm10', 0)
            ]
            colors_bar = ['blue', 'red', 'darkblue', 'darkred']
            
            bars = ax3.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black')
            ax3.axhline(y=SmartDustMote.PM25_SAFE_THRESHOLD, color='blue', linestyle='--', alpha=0.5)
            ax3.axhline(y=SmartDustMote.PM10_SAFE_THRESHOLD, color='red', linestyle='--', alpha=0.5)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax3.set_ylabel('Particle Concentration (ug/m3)')
            ax3.set_title('Pollution Statistics')
            ax3.grid(True, alpha=0.3, axis='y')
        
        # Plot 4: Alert timeline
        ax4 = self.axes[1, 1]
        alerts = self.simulation.alert_system.alerts
        
        if alerts:
            alert_times = [datetime.fromisoformat(a['timestamp']) for a in alerts[-20:]]
            severities = [a['severity'] for a in alerts[-20:]]
            severity_numeric = {'LOW': 1, 'MODERATE': 2, 'HIGH': 3, 'CRITICAL': 4}
            severity_values = [severity_numeric.get(s, 0) for s in severities]
            
            ax4.scatter(alert_times, severity_values, c='red', s=100, alpha=0.7, edgecolors='black')
            ax4.set_yticks([1, 2, 3, 4])
            ax4.set_yticklabels(['LOW', 'MODERATE', 'HIGH', 'CRITICAL'])
            ax4.set_xlabel('Time')
            ax4.set_ylabel('Alert Severity')
            ax4.set_title(f'Alert Timeline (Total: {len(alerts)})')
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'No Alerts\nAll Levels Safe', 
                    ha='center', va='center', fontsize=14, color='green', 
                    transform=ax4.transAxes)
            ax4.set_title('Alert Timeline')
        
        plt.tight_layout()
    
    def plot_historical(self, data_file: str = "dust_simulation_data.json"):
        """
        Plot historical data from saved JSON file
        
        Args:
            data_file: Path to JSON file with simulation data
        """
        if not os.path.exists(data_file):
            print(f"Error: Data file '{data_file}' not found.")
            print("Please run the simulation first to generate data.")
            return
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Smart Dust Technology - Historical Data Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Time series
        ax1 = axes[0, 0]
        readings = data.get('recent_readings', [])
        if readings:
            timestamps = [datetime.fromisoformat(r['timestamp']) for r in readings]
            pm25_values = [r['pm25'] for r in readings]
            pm10_values = [r['pm10'] for r in readings]
            
            ax1.plot(timestamps, pm25_values, 'b-', label='PM2.5', linewidth=2)
            ax1.plot(timestamps, pm10_values, 'r-', label='PM10', linewidth=2)
            ax1.axhline(y=SmartDustMote.PM25_SAFE_THRESHOLD, color='b', linestyle='--', alpha=0.5)
            ax1.axhline(y=SmartDustMote.PM10_SAFE_THRESHOLD, color='r', linestyle='--', alpha=0.5)
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Particle Concentration (ug/m3)')
            ax1.set_title('Dust Levels Over Time')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # Plot 2: Statistics
        ax2 = axes[0, 1]
        stats = data.get('statistics', {})
        if stats:
            categories = ['Avg PM2.5', 'Avg PM10', 'Max PM2.5', 'Max PM10']
            values = [
                stats.get('avg_pm25', 0),
                stats.get('avg_pm10', 0),
                stats.get('max_pm25', 0),
                stats.get('max_pm10', 0)
            ]
            colors_bar = ['blue', 'red', 'darkblue', 'darkred']
            
            bars = ax2.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black')
            ax2.axhline(y=SmartDustMote.PM25_SAFE_THRESHOLD, color='blue', linestyle='--', alpha=0.5)
            ax2.axhline(y=SmartDustMote.PM10_SAFE_THRESHOLD, color='red', linestyle='--', alpha=0.5)
            
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax2.set_ylabel('Particle Concentration (ug/m3)')
            ax2.set_title('Pollution Statistics')
            ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Pollution map
        ax3 = axes[1, 0]
        pollution_map = data.get('pollution_map', {})
        
        x_coords = []
        y_coords = []
        pm25_values_map = []
        colors = []
        
        for mote_id, mote_data in pollution_map.items():
            x_coords.append(mote_data['location'][0])
            y_coords.append(mote_data['location'][1])
            pm25_values_map.append(mote_data['pm25'])
            colors.append('red' if mote_data['status'] == 'UNSAFE' else 'green')
        
        if x_coords:
            ax3.scatter(x_coords, y_coords, c=colors, s=[v*10 for v in pm25_values_map], 
                       alpha=0.6, edgecolors='black', linewidths=1)
            for i, mote_id in enumerate(pollution_map.keys()):
                ax3.annotate(mote_id, (x_coords[i], y_coords[i]), fontsize=8)
        
        ax3.set_xlabel('X Coordinate')
        ax3.set_ylabel('Y Coordinate')
        ax3.set_title('Pollution Map')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Alerts summary
        ax4 = axes[1, 1]
        alerts = data.get('alerts', [])
        
        if alerts:
            severity_counts = {}
            for alert in alerts:
                severity = alert.get('severity', 'UNKNOWN')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            severities = list(severity_counts.keys())
            counts = list(severity_counts.values())
            colors_pie = ['yellow', 'orange', 'red', 'darkred'][:len(severities)]
            
            ax4.pie(counts, labels=severities, autopct='%1.1f%%', colors=colors_pie, startangle=90)
            ax4.set_title(f'Alerts by Severity (Total: {len(alerts)})')
        else:
            ax4.text(0.5, 0.5, 'No Alerts\nAll Levels Safe', 
                    ha='center', va='center', fontsize=14, color='green', 
                    transform=ax4.transAxes)
            ax4.set_title('Alerts Summary')
        
        plt.tight_layout()
        plt.show()


def main():
    """Main function for visualization"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--historical':
        # Plot historical data
        visualizer = DustVisualizer(None)
        visualizer.plot_historical()
    else:
        # Run real-time visualization
        print("\n" + "=" * 60)
        print("SMART DUST VISUALIZATION")
        print("=" * 60)
        print("\nStarting real-time visualization...")
        print("Close the plot window to stop.\n")
        
        simulation = SmartDustSimulation(num_motes=5)
        visualizer = DustVisualizer(simulation)
        visualizer.plot_real_time(duration=120, update_interval=2)


if __name__ == "__main__":
    main()

