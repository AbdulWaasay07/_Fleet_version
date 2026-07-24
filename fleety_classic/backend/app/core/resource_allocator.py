"""
AI-Powered Resource Allocator
Matches incoming orders with available drivers and vehicles using intelligent scoring
"""
import random
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Driver:
    id: str
    name: str
    status: str  # AVAILABLE, BUSY, OFF_DUTY
    location: dict
    rating: float
    hours_worked: float
    assigned_vehicle: Optional[str] = None

@dataclass
class Vehicle:
    id: str
    type: str  # VAN, TRUCK, CAR
    status: str  # AVAILABLE, IN_USE, MAINTENANCE
    location: dict
    fuel_level: float
    capacity: float
    assigned_driver: Optional[str] = None

class AIResourceAllocator:
    def __init__(self):
        self.drivers: List[Driver] = []
        self.vehicles: List[Vehicle] = []
        self.allocation_history = []
        
    def initialize_fleet(self):
        """Initialize 70 drivers and 70 vehicles"""
        # Create 70 drivers
        first_names = ["Alex", "Maria", "James", "Priya", "Mohammed", "Sarah", "Carlos", "Emily", "David", "Lisa", 
                      "Ahmed", "Jennifer", "Michael", "Ana", "Robert", "Fatima", "John", "Yuki", "Chris", "Nina",
                      "Omar", "Sophie", "Daniel", "Isabella", "Kevin", "Wei", "Emma", "Lucas", "Olivia", "Ryan"]
        last_names = ["Chen", "Garcia", "Wilson", "Patel", "Ali", "Johnson", "Rodriguez", "Zhang", "Kim", "Brown",
                     "Hassan", "Lee", "Smith", "Silva", "Taylor", "Khan", "Davis", "Tanaka", "Anderson", "Ivanova",
                     "Farooq", "Martin", "Park", "Rossi", "O'Brien", "Wang", "Jones", "Miller", "Lopez", "Gonzalez"]
        
        locations = [
            {"lat": 37.7749, "lon": -122.4194},  # LOCATION A
            {"lat": 37.8044, "lon": -122.2711},  # LOCATION B
            {"lat": 37.3382, "lon": -121.8863},  # LOCATION C
        ]
        
        for i in range(70):
            name = f"{random.choice(first_names)} {random.choice(last_names)}"
            self.drivers.append(Driver(
                id=f"D{i+1:03d}",
                name=name,
                status="AVAILABLE",
                location=random.choice(locations),
                rating=random.uniform(4.2, 5.0),
                hours_worked=random.uniform(0, 4)
            ))
        
        # Create 70 vehicles with diverse types
        vehicle_types = ["VAN", "TRUCK", "CAR", "BIKE", "SCOOTER", "DRONE"]
        for i in range(70):
            v_type = random.choice(vehicle_types)
            capacity = random.uniform(500, 1000)
            if v_type in ["BIKE", "SCOOTER"]: capacity = random.uniform(10, 50)
            if v_type == "DRONE": capacity = random.uniform(1, 10)
            if v_type == "TRUCK": capacity = random.uniform(1000, 5000)
            
            self.vehicles.append(Vehicle(
                id=f"V{i+1:03d}",
                type=v_type,
                status="AVAILABLE",
                location=random.choice(locations),
                fuel_level=random.uniform(60, 100),
                capacity=capacity
            ))
        
        print(f"Fleet initialized: {len(self.drivers)} drivers, {len(self.vehicles)} vehicles")
    
    def allocate_resources(self, order_id: str, origin: dict, destination: dict, payload: float):
        """
        AI-powered allocation: Find best driver-vehicle pair for the order
        Returns: (driver, vehicle, score, reasoning)
        """
        available_drivers = [d for d in self.drivers if d.status == "AVAILABLE"]
        available_vehicles = [v for v in self.vehicles if v.status == "AVAILABLE"]
        
        if not available_drivers or not available_vehicles:
            return None, None, 0, "No resources available"
        
        best_score = -1
        best_driver = None
        best_vehicle = None
        best_reasoning = ""
        
        # AI Scoring Algorithm
        for driver in available_drivers:
            for vehicle in available_vehicles:
                # Calculate distance from origin
                dist_to_origin = abs(driver.location["lat"] - origin["lat"]) + abs(driver.location["lon"] - origin["lon"])
                
                # Scoring factors
                proximity_score = max(0, 1 - dist_to_origin * 10)  # Closer is better
                driver_rating_score = driver.rating / 5.0
                vehicle_fuel_score = vehicle.fuel_level / 100.0
                capacity_score = 1.0 if vehicle.capacity >= payload else 0.5
                fatigue_score = max(0, 1 - driver.hours_worked / 8.0)  # Less tired is better
                
                # Weighted total score
                total_score = (
                    proximity_score * 0.35 +
                    driver_rating_score * 0.20 +
                    vehicle_fuel_score * 0.15 +
                    capacity_score * 0.20 +
                    fatigue_score * 0.10
                )
                
                if total_score > best_score:
                    best_score = total_score
                    best_driver = driver
                    best_vehicle = vehicle
                    best_reasoning = f"Proximity:{proximity_score:.2f} Rating:{driver_rating_score:.2f} Fuel:{vehicle_fuel_score:.2f}"
        
        # Mark as allocated
        if best_driver and best_vehicle:
            best_driver.status = "BUSY"
            best_driver.assigned_vehicle = best_vehicle.id
            best_vehicle.status = "IN_USE"
            best_vehicle.assigned_driver = best_driver.id
            
            self.allocation_history.append({
                "order_id": order_id,
                "driver": best_driver.id,
                "vehicle": best_vehicle.id,
                "score": best_score,
                "reasoning": best_reasoning
            })
        
        return best_driver, best_vehicle, best_score, best_reasoning
    
    def release_resources(self, driver_id: str, vehicle_id: str):
        """Release driver and vehicle after order completion"""
        for driver in self.drivers:
            if driver.id == driver_id:
                driver.status = "AVAILABLE"
                driver.assigned_vehicle = None
        
        for vehicle in self.vehicles:
            if vehicle.id == vehicle_id:
                vehicle.status = "AVAILABLE"
                vehicle.assigned_driver = None

    def get_available_counts(self):
        """Return counts of available resources"""
        free_drivers = sum(1 for d in self.drivers if d.status == "AVAILABLE")
        free_vehicles = sum(1 for v in self.vehicles if v.status == "AVAILABLE")
        return {
            "free_drivers": free_drivers, 
            "total_drivers": len(self.drivers),
            "free_vehicles": free_vehicles,
            "total_vehicles": len(self.vehicles)
        }

# Global instance
allocator = AIResourceAllocator()
