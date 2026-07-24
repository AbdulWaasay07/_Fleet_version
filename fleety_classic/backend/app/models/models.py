from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.core.database import Base
import datetime

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_fuel = Column(Float, default=0.0)
    total_distance = Column(Float, default=0.0)
    status = Column(String, default="RUNNING")

class MetricLog(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    vehicle_id = Column(String)
    speed = Column(Float)
    traffic_factor = Column(Float)
    rl_action = Column(Integer)
