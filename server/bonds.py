import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pyodbc
import asyncio
from typing import List
from datetime import datetime

app = FastAPI()

# Mock Database Connection
def get_db_connection():
    # Replace with actual connection details
    connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                 'SERVER=your_server;'
                                 'DATABASE=your_db;'
                                 'UID=your_user;'
                                 'PWD=your_password')
    return connection

# Pydantic models for API requests and responses
class Bond(BaseModel):
    id: int
    sector: str
    maturity: str
    rating: str
    ticker: str
    isin: str
    buySkew: float
    sellSkew: float
    dnt: str

class BulkUpdateRequest(BaseModel):
    buySkew: float
    sellSkew: float
    dnt: str

# Initialize a WebSocket manager for broadcasting
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = WebSocketManager()

# Simulated list of traders
traders = [
    {"id": "1", "name": "Trader A"},
    {"id": "2", "name": "Trader B"},
    {"id": "3", "name": "Trader C"}
]

# Simulated data for bonds
bonds = [
    {"id": 1, "sector": "Tech", "maturity": "2025-12-01", "rating": "AAA", "ticker": "AAPL", "isin": "US0378331005", "buySkew": 0.01, "sellSkew": 0.02, "dnt": "N"},
    {"id": 2, "sector": "Tech", "maturity": "2026-05-01", "rating": "AA", "ticker": "GOOG", "isin": "US02079K3059", "buySkew": 0.02, "sellSkew": 0.03, "dnt": "Y"},
    {"id": 3, "sector": "Finance", "maturity": "2027-11-01", "rating": "BBB", "ticker": "MSFT", "isin": "US5949181045", "buySkew": 0.03, "sellSkew": 0.04, "dnt": "N"}
]

@app.on_event("startup")
async def startup_event():
    print("Backend started")

# API to fetch all bonds
@app.get("/bonds/", response_model=List[Bond])
async def get_bonds():
    return bonds

# API to update bond data (single bond)
@app.post("/bonds/{bond_id}")
async def update_bond(bond_id: int, bond: Bond):
    # Update logic would interact with the database here
    for b in bonds:
        if b['id'] == bond_id:
            b.update(bond.dict())
            # Here you would update the database as well
            return {"message": "Bond updated successfully"}
    return JSONResponse(status_code=404, content={"message": "Bond not found"})

# API to bulk update skew values
@app.patch("/bulk-update/")
async def bulk_update(update: BulkUpdateRequest):
    # Mock updating bonds
    for bond in bonds:
        bond['buySkew'] = update.buySkew
        bond['sellSkew'] = update.sellSkew
        bond['dnt'] = update.dnt
        # Here you would perform database update queries as well
    # Broadcast the update to all WebSocket clients
    await manager.broadcast(f"Bulk update applied: Buy Skew: {update.buySkew}, Sell Skew: {update.sellSkew}, DNT: {update.dnt}")
    return {"message": "Bulk update applied"}

# WebSocket route to listen to updates in real time
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # You can listen for incoming messages if necessary
            data = await websocket.receive_text()
            print(f"Received data: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")

# Start the FastAPI app (you can change this to uvicorn if needed)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
