"""
CSV Trip Logger - Stores all trip details for analysis
"""
import csv
import os
from datetime import datetime
from pathlib import Path

class TripLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create CSV file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.csv_file = self.log_dir / f"trips_{timestamp}.csv"
        
        # Initialize CSV with headers
        self.headers = [
            'timestamp',
            'order_id',
            'driver_id',
            'driver_name',
            'vehicle_id',
            'vehicle_type',
            'origin_lat',
            'origin_lon',
            'destination_lat',
            'destination_lon',
            'payload',
            'allocation_score',
            'allocation_reasoning',
            'route_waypoints',
            'estimated_distance_km',
            'driver_rating',
            'vehicle_fuel_level',
            'driver_hours_worked',
            'status'
        ]
        
        # Create file and write headers
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
        
        print(f"📊 CSV Logger initialized: {self.csv_file}")
    
    def log_trip(self, trip_data):
        """
        Log a trip to CSV
        trip_data should contain: order_id, driver, vehicle, origin, destination, 
        payload, score, reasoning, route_length
        """
        try:
            row = {
                'timestamp': datetime.now().isoformat(),
                'order_id': trip_data.get('order_id', ''),
                'driver_id': trip_data.get('driver_id', ''),
                'driver_name': trip_data.get('driver_name', ''),
                'vehicle_id': trip_data.get('vehicle_id', ''),
                'vehicle_type': trip_data.get('vehicle_type', ''),
                'origin_lat': trip_data.get('origin_lat', 0),
                'origin_lon': trip_data.get('origin_lon', 0),
                'destination_lat': trip_data.get('destination_lat', 0),
                'destination_lon': trip_data.get('destination_lon', 0),
                'payload': trip_data.get('payload', 0),
                'allocation_score': trip_data.get('allocation_score', 0),
                'allocation_reasoning': trip_data.get('allocation_reasoning', ''),
                'route_waypoints': trip_data.get('route_waypoints', 0),
                'estimated_distance_km': trip_data.get('estimated_distance_km', 0),
                'driver_rating': trip_data.get('driver_rating', 0),
                'vehicle_fuel_level': trip_data.get('vehicle_fuel_level', 0),
                'driver_hours_worked': trip_data.get('driver_hours_worked', 0),
                'status': trip_data.get('status', 'DISPATCHED')
            }
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writerow(row)
                
        except Exception as e:
            print(f"❌ CSV logging error: {e}")

# Global instance
trip_logger = TripLogger()
