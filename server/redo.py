from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import pyodbc
import uuid

app = FastAPI()
connection_string = "your_connection_string_here"

class SkewUpdate(BaseModel):
    isin: str
    column: str
    new_value: str

class SkewBulkUpdateRequest(BaseModel):
    user_id: str
    updates: List[SkewUpdate]
    client_last_seen_map: Optional[Dict[str, datetime]] = None

class UndoRedoRequest(BaseModel):
    user_id: str

@app.post("/skews_bulk_update")
async def bulk_update_skews(req: SkewBulkUpdateRequest):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        now = datetime.utcnow()
        responses = []
        group_id = str(uuid.uuid4())

        for update in req.updates:
            if update.column not in ["skew", "crb_mode"]:
                continue

            cursor.execute("SELECT 1 FROM skew_bonds WHERE isin = ?", (update.isin,))
            if not cursor.fetchone():
                continue

            cursor.execute(f"SELECT {update.column}, last_updated_at FROM skew_skews WHERE isin = ?", (update.isin,))
            result = cursor.fetchone()

            if result:
                old_value, last_updated_at = result
                last_seen = req.client_last_seen_map.get(update.isin) if req.client_last_seen_map else None
                conflict = last_updated_at and last_seen and last_updated_at > last_seen

                cursor.execute(
                    f"UPDATE skew_skews SET {update.column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
                    (update.new_value, req.user_id, now, update.isin)
                )
            else:
                old_value = None
                conflict = False
                skew = update.new_value if update.column == "skew" else None
                crb_mode = update.new_value if update.column == "crb_mode" else None

                cursor.execute(
                    "INSERT INTO skew_skews (isin, skew, crb_mode, last_updated_by, last_updated_at) VALUES (?, ?, ?, ?, ?)",
                    (update.isin, skew, crb_mode, req.user_id, now)
                )

            cursor.execute(
                "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (update.isin, update.column, old_value, update.new_value, req.user_id, now, group_id)
            )
            cursor.execute(
                "INSERT INTO undo_stack (user_id, isin, column_name, old_value, new_value, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (req.user_id, update.isin, update.column, old_value, update.new_value, now, group_id)
            )
            responses.append({
                "isin": update.isin,
                "column": update.column,
                "new_value": update.new_value,
                "conflict": conflict
            })

        conn.commit()
        return {"status": "bulk_success", "updated": responses}

@app.post("/skews_undo")
async def undo_skews(req: UndoRedoRequest):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        now = datetime.utcnow()

        cursor.execute(
            "SELECT TOP 1 group_id FROM undo_stack WHERE user_id = ? ORDER BY timestamp DESC",
            (req.user_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No undo actions available.")

        group_id = row[0]

        cursor.execute(
            "SELECT isin, column_name, old_value, new_value FROM undo_stack WHERE group_id = ?",
            (group_id,)
        )
        changes = cursor.fetchall()

        for isin, column, old_value, new_value in changes:
            cursor.execute(
                f"UPDATE skew_skews SET {column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
                (old_value, req.user_id, now, isin)
            )
            cursor.execute(
                "INSERT INTO redo_stack (user_id, isin, column_name, old_value, new_value, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (req.user_id, isin, column, new_value, old_value, now, group_id)
            )

        cursor.execute("DELETE FROM undo_stack WHERE group_id = ?", (group_id,))
        conn.commit()
        return {"status": "undo_success"}

@app.post("/skews_redo")
async def redo_skews(req: UndoRedoRequest):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        now = datetime.utcnow()

        cursor.execute(
            "SELECT TOP 1 group_id FROM redo_stack WHERE user_id = ? ORDER BY timestamp DESC",
            (req.user_id,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="No redo actions available.")

        group_id = row[0]

        cursor.execute(
            "SELECT isin, column_name, old_value, new_value FROM redo_stack WHERE group_id = ?",
            (group_id,)
        )
        changes = cursor.fetchall()

        for isin, column, old_value, new_value in changes:
            cursor.execute(
                f"UPDATE skew_skews SET {column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
                (new_value, req.user_id, now, isin)
            )
            cursor.execute(
                "INSERT INTO undo_stack (user_id, isin, column_name, old_value, new_value, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (req.user_id, isin, column, old_value, new_value, now, group_id)
            )

        cursor.execute("DELETE FROM redo_stack WHERE group_id = ?", (group_id,))
        conn.commit()
        return {"status": "redo_success"}