# Smart Dust Technology Simulation System

A Python-based simulation system that demonstrates Smart Dust Technology for environmental dust detection and pollution monitoring.

## 🌪️ Overview

This project simulates the working of Smart Dust Technology using virtual sensor nodes (motes) that generate, process, and analyze dust/pollution data. The system demonstrates:

- **Sensing**: Virtual Smart Dust motes generate realistic dust and pollution readings
- **Analysis**: Real-time data processing and pollution level analysis
- **Visualization**: Interactive graphs and charts showing dust levels over time
- **Alert Generation**: Automatic alerts when pollution exceeds safe thresholds

## 📋 Features

### Core Components

1. **SmartDustMote**: Simulates individual dust sensor nodes
   - Generates PM2.5 and PM10 particle readings
   - Monitors temperature and humidity
   - Tracks location-based pollution levels

2. **DataProcessor**: Analyzes collected sensor data
   - Calculates statistics (average, max, min)
   - Determines pollution status (SAFE/UNSAFE)
   - Creates pollution maps

3. **AlertSystem**: Monitors and generates alerts
   - Threshold-based alert generation
   - Severity classification (LOW, MODERATE, HIGH, CRITICAL)
   - Alert history tracking

4. **SmartDustSimulation**: Main orchestration system
   - Manages multiple virtual motes
   - Coordinates data collection and processing
   - Provides real-time monitoring

5. **DustVisualizer**: Data visualization
   - Real-time updating plots
   - Historical data analysis
   - Pollution maps and statistics

## 🚀 Installation

1. **Clone or download this project**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Basic Simulation

Run the main simulation:

```bash
python smart_dust_system.py
```

This will:
- Create 5 virtual Smart Dust motes
- Run simulation for 60 seconds
- Collect dust readings every 2 seconds
- Generate alerts when pollution exceeds thresholds
- Save data to `dust_simulation_data.json`

### Real-Time Visualization

Run with live updating graphs:

```bash
python visualization.py
```

This opens a window with 4 real-time plots:
- Dust levels over time (PM2.5 and PM10)
- Pollution map showing mote locations
- Statistics bar chart
- Alert timeline

### Historical Data Visualization

After running a simulation, visualize saved data:

```bash
python visualization.py --historical
```

## 📊 Understanding the Output

### Pollution Thresholds

The system uses WHO (World Health Organization) guidelines:
- **PM2.5 Safe Threshold**: 25.0 μg/m³
- **PM10 Safe Threshold**: 50.0 μg/m³

### Alert Severity Levels

- **LOW**: Slightly above threshold
- **MODERATE**: Moderately elevated (PM2.5: 25-35, PM10: 50-70)
- **HIGH**: High pollution (PM2.5: 35-50, PM10: 70-100)
- **CRITICAL**: Critical levels (PM2.5: >50, PM10: >100)

### Output Files

- `dust_simulation_data.json`: Contains all collected readings, statistics, pollution map, and alerts

## 🔧 Customization

### Adjust Number of Motes

Edit `smart_dust_system.py`:

```python
simulation = SmartDustSimulation(num_motes=10)  # Change from 5 to 10
```

### Change Sampling Interval

Modify the `sampling_interval` in `SmartDustSimulation.__init__()`:

```python
self.sampling_interval = 1.0  # Sample every 1 second instead of 2
```

### Adjust Simulation Duration

```python
simulation.start_simulation(duration=120)  # Run for 2 minutes
```

### Modify Pollution Thresholds

Edit thresholds in `SmartDustMote` class:

```python
PM25_SAFE_THRESHOLD = 30.0  # Change threshold
PM10_SAFE_THRESHOLD = 60.0
```

## 📁 Project Structure

```
dust project/
├── smart_dust_system.py    # Main simulation system
├── visualization.py        # Visualization module
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── dust_simulation_data.json  # Generated data file (after running)
```

## 🎯 Key Features Demonstrated

✅ **Sensing**: Virtual motes generate realistic dust data  
✅ **Data Collection**: Continuous monitoring from multiple sensor nodes  
✅ **Analysis**: Real-time processing and statistical analysis  
✅ **Alert Generation**: Automatic alerts when thresholds are exceeded  
✅ **Visualization**: Multiple chart types showing different aspects of data  
✅ **Pollution Mapping**: Spatial visualization of pollution levels  

## 🔬 Technical Details

- **Language**: Python 3.7+
- **Key Libraries**: 
  - `matplotlib` for visualization
  - `dataclasses` for data structures
  - `collections.deque` for efficient data storage
  - `threading` for concurrent operations

## 📝 Example Output

```
🌪️  SMART DUST SIMULATION SYSTEM STARTED
============================================================
Active Motes: 5
Sampling Interval: 2.0 seconds
Duration: 60 seconds
============================================================

Monitoring dust levels...

🚨 ⚠️ MODERATE ALERT at Mote MOTE-003: PM2.5: 28.5 μg/m³ (threshold: 25.0)
   Location: (45.2, 67.8) | Time: 2024-01-15T10:30:45

📊 Status Update - 10:30:50
   Total Readings: 25
   Average PM2.5: 18.5 μg/m³
   Average PM10: 35.2 μg/m³
   Max PM2.5: 32.1 μg/m³
   Max PM10: 58.3 μg/m³
   ⚠️  Recent Alerts: 2
```

## 🤝 Contributing

This is a simulation project for educational purposes. Feel free to extend it with:
- Additional sensor types (CO2, NO2, etc.)
- Machine learning for pollution prediction
- Web dashboard interface
- Database storage for historical data
- Network simulation for mote communication

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Note**: This is a software simulation and does not require physical hardware. All sensor data is generated programmatically to demonstrate the Smart Dust Technology concept.

