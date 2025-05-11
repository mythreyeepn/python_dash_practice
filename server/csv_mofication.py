
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

class SkewUpdateRequest(BaseModel):
    isin: str
    column: str
    new_value: float
    user_id: int
    client_last_seen: datetime

@router.post("/skews/update")
async def update_skew(req: SkewUpdateRequest):
    if req.column not in ["buy_skew", "sell_skew"]:
        raise HTTPException(status_code=400, detail="Invalid column")

    result = db.query(
        f"SELECT {req.column}, last_updated_at FROM skew_skews WHERE isin = ?", (req.isin,)
    ).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Bond not found")

    old_value, last_updated_at = result
    now = datetime.utcnow()

    conflict = last_updated_at and req.client_last_seen and last_updated_at > req.client_last_seen

    db.execute(
        f"UPDATE skew_skews SET {req.column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
        (req.new_value, req.user_id, now, req.isin)
    )

    group_id = str(uuid.uuid4())
    db.execute(
        "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (req.isin, req.column, old_value, req.new_value, req.user_id, now, group_id)
    )

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