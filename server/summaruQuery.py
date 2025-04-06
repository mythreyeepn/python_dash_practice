import json
from datetime import datetime
from typing import Optional
import pyodbc

# In-memory store (optional for caching)
pt_store = {}

# DB connection (adjust your details)
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=your_server;"
        "DATABASE=your_db;"
        "UID=your_username;"
        "PWD=your_password"
    )


# ----------------- SQL HELPERS -----------------

async def get_pt_by_id_from_sql(pt_id: str) -> Optional[dict]:
    """Fetch existing PT row from SQL by PT ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data FROM pt_results WHERE pt_id = ?", pt_id)
        row = cursor.fetchone()
        if row:
            return {"data": json.loads(row[0])}
        return None


async def insert_pt_data_to_sql(pt_id: str, pt_name: str, pt_date: str, data: list):
    """Insert a new PT row into SQL."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pt_results (pt_id, pt_name, pt_date, data)
            VALUES (?, ?, ?, ?)
        """, pt_id, pt_name, pt_date, json.dumps(data))
        conn.commit()
        print(f"Inserted new PT {pt_id} into SQL.")


async def update_pt_data_in_sql(pt_id: str, data: list):
    """Update an existing PT row's data field."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pt_results SET data = ? WHERE pt_id = ?
        """, json.dumps(data), pt_id)
        conn.commit()
        print(f"Updated PT {pt_id} in SQL.")


# ----------------- UPSERT METHOD -----------------

async def upsert_pt_data_to_sql(pt_id: str, pt_name: str, pt_date: str, new_data: dict):
    """Insert or update PT data array in SQL."""
    print(f"Upserting PT {pt_id}")

    existing = await get_pt_by_id_from_sql(pt_id)

    if existing:
        data_array = existing["data"]
        data_array.append(new_data)
        await update_pt_data_in_sql(pt_id, data_array)
    else:
        await insert_pt_data_to_sql(pt_id, pt_name, pt_date, [new_data])


# ----------------- MAIN INSERT CALLS -----------------

async def insert_owic_result(pt_id: str, owic_result: dict, pt_name: str):
    """Handle OWIC insert."""
    pt_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    await upsert_pt_data_to_sql(pt_id, pt_name, pt_date, owic_result)


async def insert_bwic_result(pt_id: str, bwic_result: dict, pt_name: str):
    """Handle BWIC insert."""
    pt_date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    await upsert_pt_data_to_sql(pt_id, pt_name, pt_date, bwic_result)
