
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

router = APIRouter()

class UndoRequest(BaseModel):
    user_id: str

@router.post("/skews_undo")
async def undo_skews(req: UndoRequest):
    cursor = conn.cursor()
    now = datetime.utcnow()

    # Step 1: Get most recent group_id for this user
    cursor.execute(
        "SELECT TOP 1 group_id FROM skew_change_log WHERE user_id = ? ORDER BY timestamp DESC",
        (req.user_id,)
    )
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="No actions to undo.")

    group_id = row[0]

    # Step 2: Get all changes in that group
    cursor.execute(
        "SELECT isin, column_name, old_value, new_value FROM skew_change_log WHERE group_id = ?",
        (group_id,)
    )
    changes = cursor.fetchall()

    reverted = []
    conflicts = []

    for isin, column, old_value, new_value in changes:
        # Step 3: Check if this user’s value is still latest
        cursor.execute(
            f"SELECT {column}, last_updated_by FROM skew_skews WHERE isin = ?",
            (isin,)
        )
        result = cursor.fetchone()
        if not result:
            continue

        current_value, last_updated_by = result

        if str(current_value) != str(new_value) or last_updated_by != req.user_id:
            # Someone else has changed this since → skip
            conflicts.append({
                "isin": isin,
                "column": column,
                "latest_value": current_value,
                "reason": "Value has been updated by another user after your change."
            })
            continue

        # Step 4: Apply the undo
        cursor.execute(
            f"UPDATE skew_skews SET {column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
            (old_value, req.user_id, now, isin)
        )

        # Step 5: Log the undo
        new_group_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (isin, column, new_value, old_value, req.user_id, now, new_group_id)
        )

        # Step 6: Broadcast undo as orange highlight
        await pubsub_manager.publish(
            channel="trader-skews",
            message={
                "event": "skew_updated",
                "isin": isin,
                "column": column,
                "new_value": old_value,
                "user_id": req.user_id,
                "timestamp": now.isoformat(),
                "conflict": False,
                "highlight": {
                    "color": "orange",
                    "expires_at": now.isoformat()
                }
            }
        )

        reverted.append({
            "isin": isin,
            "column": column,
            "new_value": old_value
        })

    conn.commit()
    return {
        "status": "partial_undo" if conflicts else "undo_success",
        "reverted": reverted,
        "conflicts": conflicts
    }
