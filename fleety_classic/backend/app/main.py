from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import asyncio
from app.api.endpoints import router
from app.state import state

app = FastAPI(title="Fleety AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Initialize fleet resources
    from app.core.resource_allocator import allocator
    allocator.initialize_fleet()
    print("Starting simulation loop...")
    asyncio.create_task(simulation_loop())

async def simulation_loop():
    while True:
        start_time = time.time()
        # 1. Update Physics
        state.simulation.update()
        
        # 2. Update Environment (Traffic)
        state.environment.update()
        
        # 3. Broadcast State
        sim_state = state.simulation.get_state()
        # Convert to dict for JSON serialization
        await state.ws_manager.broadcast(sim_state.dict())
        
        # Maintain Tick Rate (e.g. 1 tick per second)
        elapsed = time.time() - start_time
        sleep_time = max(0, 1.0 - elapsed)
        await asyncio.sleep(sleep_time)

@app.get("/")
def read_root():
    return {"status": "online", "system": "Fleety AI", "timestamp": time.time()}

@app.get("/health")
def health_check():
    return {"status": "ok"}
