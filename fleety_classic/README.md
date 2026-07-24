# Fleety AI (Classic)

Fleety AI is an intelligent fleet management and resource allocation platform. Built originally during a high-pressure hackathon at Siddhartha University (AP), this platform simulates real-time driver and vehicle matching, traffic physics, and dynamic dispatching utilizing an AI-powered scoring algorithm and Reinforcement Learning.

## 🚀 Key Features

- **Intelligent Resource Allocator:** Automatically evaluates and matches the best driver-vehicle combination for incoming orders using a multi-factor scoring system.
- **Reinforcement Learning (RL) Routing:** Features an RL agent that optimizes delivery routes, tracking metrics like CO2 reduction, time saved, and overall efficiency.
- **Real-Time Simulation Engine:** A physics and environment engine runs in the background to simulate vehicle movement along paths, varying traffic conditions, and automatic order generation.
- **Live Telemetry Dashboard:** A React-based interactive frontend utilizing WebSockets to broadcast live vehicle positions, statuses, and AI metrics directly to an interactive map.

## 🧠 The AI Scoring Algorithm
When a new delivery order is generated, the AI Resource Allocator scores all available drivers and vehicles based on:
1. **Proximity (35%)**: Distance from the driver's current location to the origin point.
2. **Driver Rating (20%)**: Based on historical driver performance and ratings.
3. **Capacity Match (20%)**: Ensures the selected vehicle (Van, Truck, Car, Bike, Scooter, or Drone) can safely handle the payload.
4. **Vehicle Fuel/Battery (15%)**: Prioritizes vehicles with sufficient energy levels.
5. **Driver Fatigue (10%)**: Minimizes assignments to drivers approaching maximum hours worked.

## 🛠️ Tech Stack

### Backend
- **Python / FastAPI**: High-performance asynchronous API framework.
- **WebSockets**: Real-time bi-directional event broadcasting to the frontend.
- **SQLite / SQLAlchemy**: For local tracking of simulation runs and metric logs.

### Frontend
- **React 19 & Vite**: Ultra-fast frontend framework and bundler.
- **Leaflet & React-Leaflet**: For rendering the interactive fleet map.
- **Recharts**: For displaying real-time analytics and telemetry data.
- **Tailwind CSS**: For clean, modern UI styling.

## 🏁 Getting Started

To run the system locally, ensure you have **Python** and **Node.js** installed.

### Quick Start (Windows)
Simply run the included startup script from the root of the project:
```bash
.\start_fleety.bat
```
This script will automatically:
1. Activate the Python virtual environment and start the FastAPI backend server (`http://localhost:8000`).
2. Start the React frontend development server (`http://localhost:5173`).

### Manual Start
If you prefer to run the components manually in separate terminal windows:

**Backend:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```
