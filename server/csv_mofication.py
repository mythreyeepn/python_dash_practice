
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional
import uuid

router = APIRouter()

class SkewUpdateItem(BaseModel):
    isin: str
    column: str
    new_value: float

class SkewBulkUpdateRequest(BaseModel):
    updates: List[SkewUpdateItem]
    user_id: str
    client_last_seen_map: Optional[Dict[str, datetime]] = None

@router.post("/skews_bulk_update")
async def bulk_update_skews(req: SkewBulkUpdateRequest):
    cursor = conn.cursor()
    now = datetime.utcnow()
    responses = []

    for update in req.updates:
        if update.column not in ["buy_skew", "sell_skew"]:
            continue  # skip invalid columns

        # Check bond exists
        cursor.execute("SELECT 1 FROM skew_bonds WHERE isin = ?", (update.isin,))
        if not cursor.fetchone():
            continue

        # Fetch existing skew and timestamp
        cursor.execute(
            f"SELECT {update.column}, last_updated_at FROM skew_skews WHERE isin = ?",
            (update.isin,)
        )
        result = cursor.fetchone()

        if result:
            old_value, last_updated_at = result
            last_seen = req.client_last_seen_map.get(update.isin) if req.client_last_seen_map else None

            conflict = last_updated_at and last_seen and last_updated_at > last_seen

            # Update
            cursor.execute(
                f"UPDATE skew_skews SET {update.column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
                (update.new_value, req.user_id, now, update.isin)
            )
        else:
            old_value = None
            last_updated_at = None
            conflict = False

            buy_skew = update.new_value if update.column == "buy_skew" else None
            sell_skew = update.new_value if update.column == "sell_skew" else None

            cursor.execute(
                "INSERT INTO skew_skews (isin, buy_skew, sell_skew, last_updated_by, last_updated_at) VALUES (?, ?, ?, ?, ?)",
                (update.isin, buy_skew, sell_skew, req.user_id, now)
            )

        # Log change
        group_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (update.isin, update.column, old_value, update.new_value, req.user_id, now, group_id)
        )

        # WebSocket broadcast
        await pubsub_manager.publish(
            channel="trader-skews",
            message={
                "event": "skew_updated",
                "isin": update.isin,
                "column": update.column,
                "new_value": update.new_value,
                "user_id": req.user_id,
                "timestamp": now.isoformat(),
                "conflict": conflict,
                "highlight": {
                    "color": "green",
                    "expires_at": (now.isoformat())
                }
            }
        )

        responses.append({
            "isin": update.isin,
            "column": update.column,
            "new_value": update.new_value,
            "conflict": conflict
        })

    conn.commit()
    return {"status": "bulk_success", "updated": responses}
