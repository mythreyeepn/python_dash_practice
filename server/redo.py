
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class RedoRequest(BaseModel):
    user_id: str

@router.post("/skews_redo")
async def redo_skews(req: RedoRequest):
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    now = datetime.utcnow()

    # Step 1: Get the most recent group_id from redo_stack
    cursor.execute(
        "SELECT TOP 1 group_id FROM redo_stack WHERE user_id = ? ORDER BY timestamp DESC",
        (req.user_id,)
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No actions to redo.")

    group_id = row[0]

    # Step 2: Remove it from the redo stack
    cursor.execute(
        "DELETE FROM redo_stack WHERE user_id = ? AND group_id = ?",
        (req.user_id, group_id)
    )

    # Step 3: Get the changes to redo
    cursor.execute(
        "SELECT isin, column_name, new_value, old_value FROM skew_change_log WHERE group_id = ?",
        (group_id,)
    )
    changes = cursor.fetchall()

    new_group_id = str(uuid.uuid4())
    for isin, column, new_value, old_value in changes:
        # Apply redo
        cursor.execute(
            f"UPDATE skew_skews SET {column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
            (new_value, req.user_id, now, isin)
        )

        # Log the redo
        cursor.execute(
            "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (isin, column, old_value, new_value, req.user_id, now, new_group_id)
        )

        # Publish via socket
        await pubsub_manager.publish(
            channel="trader-skews",
            message={
                "event": "skew_updated",
                "isin": isin,
                "column": column,
                "new_value": new_value,
                "user_id": req.user_id,
                "timestamp": now.isoformat() + "Z",
                "highlight": {
                    "color": "green",
                    "expires_at": now.isoformat() + "Z"
                }
            }
        )

    conn.commit()
    return {"status": "redo_success", "restored_group": group_id}

# CREATE TABLE redo_stack (
#     user_id VARCHAR(50),
#     group_id VARCHAR(50),
#     timestamp DATETIME DEFAULT GETDATE(),
#     PRIMARY KEY (user_id, group_id)
# );
