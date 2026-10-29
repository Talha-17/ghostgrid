
import time
import random
from database import init_db, log_sensor_data

def simulate_sensor_stream(sensor_id="sensor_alpha_01", interval_seconds=2):
    """
    Simulates a hardware sensor stream running on an edge device.
    Generates telemetry readings and saves them locally offline.
    """
    print(f"[GhostGrid] Starting sensor daemon for [{sensor_id}]...")
    print("[GhostGrid] Press Ctrl+C to stop the sensor stream.\n")
    
    # Ensure database is ready
    init_db()
    
    try:
        while True:
            # Simulate picking up a physical reading (e.g., temperature between 20°C and 40°C)
            reading = round(random.uniform(20.0, 40.0), 2)
            status = "NORMAL" if reading < 35.0 else "WARNING_HIGH_TEMP"
            
            # Save locally using our database module
            log_sensor_data(sensor_id, reading, status)
            
            print(f"[Telemetry] Sensor: {sensor_id} | Value: {reading}°C | Status: {status} | Saved Locally (Offline)")
            
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("\n[GhostGrid] Sensor daemon stopped safely.")

if __name__ == "__main__":
    simulate_sensor_stream()