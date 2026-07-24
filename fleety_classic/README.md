# Fleety AI (Classic)

Fleety AI is an intelligent fleet management and resource allocation platform. It simulates real-time driver and vehicle matching, traffic physics, and dynamic dispatching utilizing an AI-powered scoring algorithm. 

## Features
- **AI Resource Allocator:** Automatically matches drivers to vehicles and incoming orders.
- **Real-Time Simulation:** WebSocket-based continuous updates for vehicle positions and statuses.
- **Interactive Dashboard:** React-based frontend mapping the simulation in real-time.

## Tech Stack
- **Backend:** Python, FastAPI, WebSockets
- **Frontend:** React, Leaflet Maps, Vite

## Getting Started
To run the system locally, ensure you have Python and Node.js installed, then run the startup script:

```bash
.\start_fleety.bat
```
This will automatically launch both the FastAPI backend server and the React frontend.
