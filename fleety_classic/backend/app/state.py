from app.simulation.engine import SimulationEngine
from app.simulation.environment import SimulationEnvironment
from app.api.websocket_manager import manager
from app.planning.heuristic import HeuristicPlanner

class GlobalState:
    simulation: SimulationEngine = SimulationEngine()
    environment: SimulationEnvironment = SimulationEnvironment()
    planner: HeuristicPlanner = HeuristicPlanner()
    ws_manager = manager
    watched_vehicles: set = set()

state = GlobalState()
