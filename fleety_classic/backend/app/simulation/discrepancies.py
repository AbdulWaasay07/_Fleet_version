import random
from app.schemas.simulation import Location

class DiscrepancyGenerator:
    def __init__(self):
        self.active_jams = {}  # {zone_id: severity}

    def generate_events(self):
        # Randomly create traffic jams
        if random.random() < 0.05: # 5% chance per tick to change traffic
             pass 

    def get_traffic_factor(self, location: Location) -> float:
        # Simulate traffic based on location (random for now)
        # Returns multiplier: 1.0 = Normal, 0.1 = Dead Stop
        # Let's make a "bad zone" around default start coordinates for testing
        
        # If near 37.79, -122.40 (approx center of path)
        if 37.78 < location.lat < 37.80 and -122.41 < location.lon < -122.39:
             # Random fluctuation to simulate stop-and-go
             return random.uniform(0.3, 0.8)
        
        return 1.0
