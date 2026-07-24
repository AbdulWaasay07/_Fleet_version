from typing import List
from app.schemas.simulation import Location

class HeuristicPlanner:
    def plan(self, origin: Location, destination: Location) -> List[Location]:
        # MVP: Return a straight line with 10 intermediate points
        # In real life, this uses a Graph (NetworkX or OSRM)
        
        path = [origin]
        steps = 10
        for i in range(1, steps):
            fraction = i / steps
            lat = origin.lat + (destination.lat - origin.lat) * fraction
            lon = origin.lon + (destination.lon - origin.lon) * fraction
            path.append(Location(lat=lat, lon=lon))
        
        path.append(destination)
        return path
