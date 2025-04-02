from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import qpython.qconnection as qconn
from collections import deque

app = FastAPI()

# In-memory storage for SDR trades
sdr_trades = deque(maxlen=1000)  # Stores latest trades (adjust size as needed)
seen_trade_ids = set()  # Track seen trades to avoid duplicates
latest_timestamp = None  # Track the last trade timestamp

# Function to fetch new trades from kdb
def fetch_new_trades():
    global latest_timestamp
    with qconn.QConnection(host='your_kdb_host', port=your_kdb_port, username='user', password='pass') as q:
        query = f"select from trades where executionTimestamp >= {latest_timestamp}" if latest_timestamp else "select from trades"
        result = q(query)
        if result:
            new_trades = [trade for trade in result if trade['disseminationId'] not in seen_trade_ids]
            for trade in new_trades:
                seen_trade_ids.add(trade['disseminationId'])
            
            if new_trades:
                latest_timestamp = max(trade['executionTimestamp'] for trade in new_trades)  # Update last timestamp
                sdr_trades.extend(new_trades)
            return new_trades
        return []

# WebSocket endpoint
@app.websocket("/ws/sdr")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(3)  # Fetch every 3 seconds
            new_trades = fetch_new_trades()
            if new_trades:
                await websocket.send_json(new_trades)
    except WebSocketDisconnect:
        print("WebSocket client disconnected")

# Run with: uvicorn filename:app --reload
