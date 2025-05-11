from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
import pyodbc

from pubsub_manager import InMemoryPubSubManager

app = FastAPI()
conn = pyodbc.connect("your_connection_string")
pubsub_manager = InMemoryPubSubManager()

class SkewUpdateRequest(BaseModel):
    isin: str
    column: str  # "buy_skew" or "sell_skew"
    new_value: float
    user_id: int
    client_last_seen: datetime = None  # optional for first-time edit

@app.post("/skews_update")
async def update_skew(req: SkewUpdateRequest):
    if req.column not in ["buy_skew", "sell_skew"]:
        raise HTTPException(status_code=400, detail="Invalid column")

    cursor = conn.cursor()
    now = datetime.utcnow()

    # Step 1: Try to fetch existing skew value
    cursor.execute(
        f"SELECT {req.column}, last_updated_at FROM skew_skews WHERE isin = ?",
        (req.isin,)
    )
    result = cursor.fetchone()

    if result:
        old_value, last_updated_at = result

        # Step 2: Safe Hybrid Conflict Detection
        conflict = False
        if last_updated_at and req.client_last_seen:
            if last_updated_at > req.client_last_seen:
                conflict = True

        # Step 3: Update existing skew
        cursor.execute(
            f"""
            UPDATE skew_skews
            SET {req.column} = ?, last_updated_by = ?, last_updated_at = ?
            WHERE isin = ?
            """,
            (req.new_value, req.user_id, now, req.isin)
        )

    else:
        # Step 4: Insert new skew row
        buy_skew = req.new_value if req.column == "buy_skew" else None
        sell_skew = req.new_value if req.column == "sell_skew" else None

        cursor.execute(
            """
            INSERT INTO skew_skews (isin, buy_skew, sell_skew, last_updated_by, last_updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (req.isin, buy_skew, sell_skew, req.user_id, now)
        )

        old_value = None  # No previous value
        conflict = False  # First-time insert cannot conflict

    # Step 5: Log the change
    group_id = str(uuid.uuid4())
    cursor.execute(
        """
        INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (req.isin, req.column, old_value, req.new_value, req.user_id, now, group_id)
    )

    conn.commit()

    # Step 6: WebSocket broadcast
    await pubsub_manager.publish(
        channel="trader-skews",
        message={
            "event": "skew_updated",
            "isin": req.isin,
            "column": req.column,
            "new_value": req.new_value,
            "user_id": req.user_id,
            "timestamp": now.isoformat(),
            "conflict": conflict
        }
    )

    return {
        "status": "success",
        "conflict": conflict,
        "isin": req.isin,
        "column": req.column,
        "old_value": old_value,
        "new_value": req.new_value
    }


@app.websocket("/ws/{channel}")
async def websocket_endpoint(websocket: WebSocket, channel: str):
    await websocket.accept()
    pubsub_manager.register(channel, websocket)

    try:
        while True:
            # Optional: read presence messages from client (e.g. start_edit)
            message = await websocket.receive_json()
            await pubsub_manager.publish(channel, message)  # echo to others
    except WebSocketDisconnect:
        pubsub_manager.unregister(channel, websocket)

