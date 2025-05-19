
from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class BulkSkewUpdate(BaseModel):
    user_id: str
    updates: list  # each item should have { isin, column, new_value }

@router.post("/skews_bulk_update")
async def bulk_update_skews(req: BulkSkewUpdate, background_tasks: BackgroundTasks):
    now = datetime.utcnow()
    group_id = str(uuid.uuid4())

    # ✅ Commit changes immediately
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    for update in req.updates:
        if update["column"] not in ["buy_skew", "sell_skew"]:
            continue
        cursor.execute("SELECT 1 FROM skew_bonds WHERE isin = ?", (update["isin"],))
        if not cursor.fetchone():
            continue

        cursor.execute(
            f"UPDATE skew_skews SET {update['column']} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
            (update["new_value"], req.user_id, now, update["isin"])
        )

        cursor.execute(
            "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (update["isin"], update["column"], None, update["new_value"], req.user_id, now, group_id)
        )
    conn.commit()

    # ✅ Offload WebSocket broadcast to background
    background_tasks.add_task(broadcast_bulk_updates, req.updates, req.user_id, now)

    return {"status": "accepted", "message": f"{len(req.updates)} rows queued for update."}

async def broadcast_bulk_updates(updates, user_id, timestamp):
    message = {
        "event": "bulk_skew_updated",
        "updates": []
    }
    for update in updates:
        message["updates"].append({
            "isin": update["isin"],
            "column": update["column"],
            "new_value": update["new_value"],
            "user_id": user_id,
            "timestamp": timestamp.isoformat() + "Z",
            "highlight": {
                "color": "green",
                "expires_at": timestamp.isoformat() + "Z"
            }
        })

    await pubsub_manager.publish(channel="trader-skews", message=message)



# socket.onmessage = (event) => {
#   const data = JSON.parse(event.data);
#   switch (data.event) {
#     case "bulk_skew_updated":
#       data.updates.forEach(update => {
#         const rowNode = gridRef.current.api.getRowNode(update.isin);
#         if (!rowNode) return;
#         const fullRow = { ...rowNode.data };
#         fullRow[update.column] = update.new_value;
#         fullRow.highlightStatus = {
#           ...(fullRow.highlightStatus || {}),
#           [update.column]: {
#             color: update.highlight?.color || "green",
#             expiresAt: Date.now() + 45000
#           }
#         };
#         gridRef.current.api.applyTransaction({ update: [fullRow] });
#       });
#       break;
#   }
# };
