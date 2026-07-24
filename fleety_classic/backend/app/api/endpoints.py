from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import uuid

from app.state import state
from app.schemas.simulation import Location

router = APIRouter()

class DispatchRequest(BaseModel):
    origin: Location
    destination: Location
    payload: float

@router.post("/dispatch")
async def dispatch_vehicle(req: DispatchRequest):
    from app.core.resource_allocator import allocator
    from app.core.trip_logger import trip_logger
    from datetime import datetime
    
    try:
        # 1. AI Resource Allocation
        driver, vehicle, score, reasoning = allocator.allocate_resources(
            order_id=f"ORD-{uuid.uuid4().hex[:8]}",
            origin=req.origin.dict(),
            destination=req.destination.dict(),
            payload=req.payload
        )
        
        if not driver or not vehicle:
            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "error",
                "title": "Dispatch Failed",
                "details": {"reason": "No resources available"},
                "timestamp": datetime.now().isoformat()
            })
            return {"status": "failed", "reason": "No resources available"}
        
        # Log allocation
        await state.ws_manager.broadcast({
            "type": "log",
            "log_type": "info",
            "title": "AI Resource Allocation",
            "details": {
                "Driver": f"{driver.name} ({driver.id})",
                "Vehicle": f"{vehicle.type} ({vehicle.id})",
                "Score": f"{score:.3f}",
                "Reasoning": reasoning
            },
            "timestamp": datetime.now().isoformat()
        })
        
        print(f" AI ALLOCATOR: {driver.id} + {vehicle.id} (Score: {score:.2f}) - {reasoning}")
        
        # 2. RL Route Planning
        path = state.planner.plan(req.origin, req.destination)
        
        # 3. Calculate distance
        distance_km = len(path) * 0.5  # Rough estimate
        
        # 4. Log to CSV
        trip_logger.log_trip({
            'order_id': f"{driver.id}_{vehicle.id}",
            'driver_id': driver.id,
            'driver_name': driver.name,
            'vehicle_id': vehicle.id,
            'vehicle_type': vehicle.type,
            'origin_lat': req.origin.lat,
            'origin_lon': req.origin.lon,
            'destination_lat': req.destination.lat,
            'destination_lon': req.destination.lon,
            'payload': req.payload,
            'allocation_score': score,
            'allocation_reasoning': reasoning,
            'route_waypoints': len(path),
            'estimated_distance_km': distance_km,
            'driver_rating': driver.rating,
            'vehicle_fuel_level': vehicle.fuel_level,
            'driver_hours_worked': driver.hours_worked,
            'status': 'DISPATCHED'
        })
        
        # 5. Create simulation vehicle
        sim_vehicle_id = f"v_{len(state.simulation.vehicles) + 1}"
        state.simulation.init_vehicle(sim_vehicle_id, req.origin, real_driver_id=driver.id, real_vehicle_id=vehicle.id)
        state.simulation.dispatch(sim_vehicle_id, path, f"{driver.id}_{vehicle.id}")
        
        await state.ws_manager.broadcast({
            "type": "log",
            "log_type": "success",
            "title": "Order Dispatched",
            "details": {
                "Vehicle ID": sim_vehicle_id,
                "Route": f"{len(path)} waypoints",
                "Est. Distance": f"{distance_km:.1f} km"
            },
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "status": "dispatched", 
            "vehicle_id": sim_vehicle_id,
            "driver": driver.id,
            "physical_vehicle": vehicle.id,
            "allocation_score": score,
            "route_length": len(path)
        }
    except Exception as e:
        print(f"Dispatch error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

@router.get("/state")
def get_simulation_state():
    return state.simulation.get_state()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await state.ws_manager.connect(websocket)
    try:
        while True:
            # We can receive commands from client here if needed
            data = await websocket.receive_text()
            import json
            try:
                msg = json.loads(data)
                if msg.get("type") == "watch_vehicles":
                    valid_ids = set(msg.get("ids", []))
                    state.watched_vehicles = valid_ids
                    print(f"User watching: {valid_ids}")
            except Exception as e:
                print(f"WS Input Error: {e}")
    except WebSocketDisconnect:
        state.ws_manager.disconnect(websocket)

# ANALYTICS ENDPOINTS
from app.core.database import get_db, SessionLocal
from app.models.models import SimulationRun, MetricLog
from fastapi import Depends
from sqlalchemy.orm import Session

@router.get("/analytics/runs")
def get_runs():
    db = SessionLocal()
    runs = db.query(SimulationRun).all()
    db.close()
    return runs

@router.get("/analytics/metrics/{run_id}")
def get_metrics(run_id: int):
    db = SessionLocal()
    metrics = db.query(MetricLog).filter(MetricLog.run_id == run_id).all()
    db.close()
    return metrics

# SERVER-SIDE ORDER SIMULATION
import random
import asyncio

# Auto-start simulation by default
order_simulation_active = True

@router.on_event("startup")
async def startup_simulation():
    """Start order generation automatically on startup"""
    asyncio.create_task(order_generation_loop())
    asyncio.create_task(vehicle_stats_broadcast_loop())
    asyncio.create_task(simulation_tick_loop())

@router.post("/simulate/start-orders")
async def start_order_simulation():
    """Start automatic order generation on the server"""
    global order_simulation_active
    if not order_simulation_active:
        order_simulation_active = True
        asyncio.create_task(order_generation_loop())
        return {"status": "started", "message": "Order simulation started"}
    return {"status": "already_running"}

@router.post("/simulate/stop-orders")
async def stop_order_simulation():
    """Stop automatic order generation"""
    global order_simulation_active
    order_simulation_active = False
    return {"status": "stopped"}

async def order_generation_loop():
    """Background task that generates orders continuously with random intervals"""
    global order_simulation_active
    from app.core.resource_allocator import allocator
    from datetime import datetime
    
    # Wait a bit for server to fully start
    await asyncio.sleep(5)
    
    while order_simulation_active:
        # Generate 1-3 orders (random batch)
        orders_batch = random.randint(1, 3)
        
        for _ in range(orders_batch):
            if not order_simulation_active:
                break
                
            origins = [
                Location(lat=37.7749, lon=-122.4194),
                Location(lat=37.8044, lon=-122.2711),
                Location(lat=37.3382, lon=-121.8863),
            ]
            
            destinations = [
                Location(lat=37.8044, lon=-122.2711),
                Location(lat=37.7749, lon=-122.4194),
                Location(lat=37.5485, lon=-121.9886),
            ]
            
            origin = random.choice(origins)
            destination = random.choice([d for d in destinations if d != origin])
            order_id = f"ORD-{random.randint(1000, 9999)}"
            payload = random.uniform(100, 500)
            
            # Broadcast Waiting Status if resources low
            stats = allocator.get_available_counts()
            
            # STEP 1: QUEUE
            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "info",
                "step": 1,
                "title": "Order Queued",
                "details": {
                    "Order ID": order_id,
                    "Status": "Pending Allocation",
                    "Payload": f"{payload:.1f} kg",
                    "Free Drivers": f"{stats['free_drivers']}/{stats['total_drivers']}",
                    "Free Vehicles": f"{stats['free_vehicles']}/{stats['total_vehicles']}"
                },
                "timestamp": datetime.now().isoformat(),
                "resource_stats": stats
            })
            
            # Fast queue processing for random feel
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            # STEP 2: ALLOCATION
            driver, vehicle, score, reasoning = allocator.allocate_resources(
                order_id=order_id,
                origin=origin.dict(),
                destination=destination.dict(),
                payload=payload
            )
            
            if not driver or not vehicle:
                print(f" [{order_id}] NO RESOURCES - Queue full")
                new_stats = allocator.get_available_counts()
                await state.ws_manager.broadcast({
                    "type": "log",
                    "log_type": "warning",
                    "step": 2,
                    "title": "Allocation Wait",
                    "details": {
                        "Reason": "Resources Limit Reached",
                        "Status": "Queued until resources free",
                        "Free Drivers": f"{new_stats['free_drivers']}",
                        "Free Vehicles": f"{new_stats['free_vehicles']}"
                    },
                    "timestamp": datetime.now().isoformat(),
                    "resource_stats": new_stats
                })
                # Retry sooner if random
                await asyncio.sleep(random.uniform(2, 5)) 
                continue
            
            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "success",
                "step": 2,
                "title": "Resource Allocated",
                "details": {
                    "Driver": f"{driver.name}",
                    "Vehicle": f"{vehicle.id}",
                    "Score": f"{score:.3f}"
                },
                "timestamp": datetime.now().isoformat(),
                "resource_stats": allocator.get_available_counts()
            })
            
            # STEP 3: ROUTING
            path = state.planner.plan(origin, destination)
            distance_km = len(path) * 0.5
            
            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "info",
                "step": 3,
                "title": "Route Optimized",
                "details": {
                    "Waypoints": len(path),
                    "Est. Distance": f"{distance_km:.1f} km"
                },
                "timestamp": datetime.now().isoformat()
            })

            # STEP 4: TRACKING
            sim_vehicle_id = f"v_{len(state.simulation.vehicles) + 1}"
            state.simulation.init_vehicle(sim_vehicle_id, origin, real_driver_id=driver.id, real_vehicle_id=vehicle.id)
            state.simulation.dispatch(sim_vehicle_id, path, order_id)
            
            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "success",
                "step": 4,
                "title": "Tracking Started",
                "details": {
                    "Vehicle ID": sim_vehicle_id,
                    "Status": "En Route"
                },
                "timestamp": datetime.now().isoformat()
            })

            # STEP 5 & 6: STORE
            from app.core.trip_logger import trip_logger
            trip_logger.log_trip({
                'order_id': order_id,
                'driver_id': driver.id,
                'driver_name': driver.name,
                'vehicle_id': vehicle.id,
                'vehicle_type': vehicle.type,
                'origin_lat': origin.lat,
                'origin_lon': origin.lon,
                'destination_lat': destination.lat,
                'destination_lon': destination.lon,
                'payload': payload,
                'allocation_score': score,
                'allocation_reasoning': reasoning,
                'route_waypoints': len(path),
                'estimated_distance_km': distance_km,
                'driver_rating': driver.rating,
                'vehicle_fuel_level': vehicle.fuel_level,
                'driver_hours_worked': driver.hours_worked,
                'status': 'AUTO_DISPATCHED'
            })

            await state.ws_manager.broadcast({
                "type": "log",
                "log_type": "success",
                "step": 6,
                "title": "Dispatch Finalized",
                "details": {
                    "Database": "drivers.db / trips",
                    "Status": "Persisted"
                },
                "timestamp": datetime.now().isoformat()
            })
            

        # Random interval between batches (2 to 9 seconds)
        await asyncio.sleep(random.uniform(2, 9))

async def vehicle_stats_broadcast_loop():
    """Background task to broadcast vehicle analytics frequently"""
    from app.state import state
    import random
    
    while True:
        try:
            # Broadcast even if no orders are generating, as long as vehicles exist
            vehicles = list(state.simulation.vehicles.values())
            
            selected = []
            
            # 1. Filter by User Selection
            if state.watched_vehicles:
                # Only show vehicles the user has selected
                # Filter vehicles that match the watched IDs
                selected = [v for v in vehicles if v.id in state.watched_vehicles]
            else:
                # If no selection, show nothing (per user request "only show vehicles that i selected")
                # But to avoid a broken look, we'll send an empty list which the frontend will handle
                selected = []

            analytics_data = []
            for v in selected:
                progress = 0
                if v.current_path:
                    progress = int((v.route_index / len(v.current_path)) * 100)
                
                analytics_data.append({
                    "id": v.id,
                    "real_id": v.real_vehicle_id or "—",
                    "status": v.status,
                    "speed": int(v.speed),
                    "battery": int(v.battery_level),
                    "progress": progress
                })
            
            # Always broadcast, even if empty, so frontend knows to clear/show placeholder
            await state.ws_manager.broadcast({
                "type": "vehicle_analytics",
                "data": analytics_data,
                "active_ids": [v.id for v in vehicles if v.status != "IDLE"]
            })
                
            await asyncio.sleep(1.0) # Update every second
        except Exception as e:
            print(f"Stats broadcast error: {e}")
            await asyncio.sleep(1.0)


async def simulation_tick_loop():
    """Background task to update simulation physics"""
    from app.state import state
    while True:
        try:
            await state.simulation.update()
            await asyncio.sleep(0.5) # Update physics twice a second
        except Exception as e:
            print(f"Simulation tick error: {e}")
            await asyncio.sleep(1.0)
