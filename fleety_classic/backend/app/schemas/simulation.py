from pydantic import BaseModel
from typing import List, Optional, Tuple

class Location(BaseModel):
    lat: float
    lon: float

class Order(BaseModel):
    id: str
    origin: Location
    destination: Location
    payload_weight: float
    deadline: float  # Timestamp
    status: str = "PENDING"  # PENDING, ASSIGNED, DELIVERED, CANCELLED

class VehicleState(BaseModel):
    id: str
    location: Location
    speed: float = 0.0
    heading: float = 0.0
    battery_level: float = 100.0
    capacity_used: float = 0.0
    progress: float = 0.0
    status: str = "IDLE"  # IDLE, MOVING, REROUTING, CHARGING
    current_path: List[Location] = []
    current_destination: Optional[Location] = None
    assigned_order_id: Optional[str] = None
    route_index: int = 0
    real_driver_id: Optional[str] = None
    real_vehicle_id: Optional[str] = None
    vehicle_type: str = "Generic"
    current_speed_val: float = 0.0  # Internal speed tracking for simulation
    has_accident: bool = False
    accident_severity: Optional[str] = None # LOW, MEDIUM, CRITICAL
    harsh_braking_count: int = 0
    harsh_accel_count: int = 0
    last_speed: float = 0.0
    avg_speed: float = 0.0
    stop_count: int = 0
    total_speed_sum: float = 0.0
    speed_sample_count: int = 0

class SimulationState(BaseModel):
    tick: int
    vehicles: List[VehicleState]
    active_orders: List[Order]
    pending_orders_count: int = 0
    traffic_factor: float = 1.0  # 1.0 = Normal, 0.5 = Heavy Traffic (slow)
