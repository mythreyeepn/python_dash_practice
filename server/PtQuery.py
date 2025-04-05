import asyncio
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException
from qpython import qconnection

# FastAPI app initialization
app = FastAPI()

# In-memory storage for PTs
pt_store: Dict[str, Dict] = {}

# Establish a connection to your KDB database
# Replace these details with your actual KDB connection details
kdb_conn = qconnection.QConnection(host='your_kdb_host', port=your_kdb_port)
kdb_conn.open()

# Function to perform KDB query (replace with your actual KDB queries)
async def kdb_query(query: str) -> dict:
    """Perform a KDB query using qpython."""
    try:
        # Execute the KDB query and get the result (replace this with actual query logic)
        result = kdb_conn(query)
        return {"data": result}
    except Exception as e:
        raise Exception(f"KDB query failed: {e}")

# Function to retry KDB queries in case of failure
async def retry_kdb_query(query: str, retries: int = 2) -> dict:
    """Try KDB query multiple times if it fails."""
    attempt = 0
    while attempt <= retries:
        try:
            return await kdb_query(query)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for query: {query} - Error: {e}")
            attempt += 1
            if attempt > retries:
                raise Exception(f"Failed after {retries + 1} attempts for query: {query}")
            await asyncio.sleep(2)  # Wait before retrying

# Function to insert combined OWIC and BWIC results into SQL
async def insert_combined_result_to_sql(pt_id: str, owic_result: dict, bwic_result: dict):
    """Insert combined OWIC and BWIC results into the database."""
    # Replace this with your actual SQL insert logic
    print(f"Inserting combined results for PT {pt_id} into SQL")
    print(f"OWIC Result: {owic_result}")
    print(f"BWIC Result: {bwic_result}")
    
    # After successful insert, remove the PT from the store
    pt_store.pop(pt_id, None)
    print(f"PT {pt_id} removed from store after successful insert.")

# Function to insert OWIC results into SQL (immediately after getting the response)
async def insert_owic_result_to_sql(pt_id: str, owic_result: dict, pt_name: str, pt_date: str):
    """Insert OWIC result into SQL immediately."""
    # Replace this with your actual SQL insert logic
    print(f"Inserting OWIC result for PT {pt_id} into SQL")
    print(f"OWIC Result: {owic_result}")
    
    # Add PT info to the insert (you can replace with actual fields)
    print(f"Inserting PT ID: {pt_id}, PT Name: {pt_name}, PT Date: {pt_date} along with OWIC data.")
    
    # Update pt_store with OWIC response
    pt_store[pt_id]["owic_response"] = owic_result
    pt_store[pt_id]["status"] = "owic_inserted"

# Function to update BWIC results into SQL once both OWIC and BWIC are available
async def update_bwic_result_to_sql(pt_id: str, bwic_result: dict):
    """Update BWIC result into SQL after both responses are available."""
    pt_info = pt_store.get(pt_id)
    
    if pt_info and pt_info["owic_response"]:
        # If OWIC response is available, we can proceed with the update
        print(f"Updating BWIC result for PT {pt_id} into SQL")
        print(f"BWIC Result: {bwic_result}")
        
        # Update SQL with combined OWIC and BWIC results (this is where you combine the data)
        await insert_combined_result_to_sql(pt_id, pt_info["owic_response"], bwic_result)
        pt_store[pt_id]["status"] = "completed"  # Mark PT as completed

# Function to process the PT, handle OWIC and BWIC queries, and manage the store
async def process_pt(pt: Dict):
    """Process a PT by querying OWIC and BWIC concurrently."""
    pt_id = pt["pt_id"]
    pt_name = pt["pt_name"]
    pt_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Adding PT date as now()

    # Store PT in memory with its basic info
    pt_store[pt_id] = {"pt_name": pt_name, "pt_date": pt_date, "owic_response": None, "bwic_response": None, "status": "processing"}

    # Query OWIC and BWIC concurrently (classify bonds based on notional)
    owic_bonds = [bond for bond in pt["bonds"] if bond["notional"] > 0]
    bwic_bonds = [bond for bond in pt["bonds"] if bond["notional"] < 0]

    owic_query = f"select from owic where bonds in {owic_bonds}"  # Replace with actual query
    bwic_query = f"select from bwic where bonds in {bwic_bonds}"  # Replace with actual query

    # Asynchronous queries for OWIC and BWIC
    owic_task = asyncio.create_task(retry_kdb_query(owic_query))
    bwic_task = asyncio.create_task(retry_kdb_query(bwic_query))

    # Wait for the responses to be received
    owic_response = await owic_task
    bwic_response = await bwic_task

    # Handle OWIC response - Insert immediately into SQL
    await insert_owic_result_to_sql(pt_id, owic_response, pt_name, pt_date)

    # Handle BWIC response - Update the record once BWIC is received
    if bwic_response:
        await update_bwic_result_to_sql(pt_id, bwic_response)

# Endpoint to receive a new PT and start processing
@app.post("/process_pt/")
async def process_new_pt(pt: Dict):
    """Receive a new PT, process it and return status."""
    try:
        await process_pt(pt)
        return {"status": "success", "message": "PT processing started"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API to check failed PTs (those that couldn't be processed successfully)
@app.get("/failed_pts/")
async def get_failed_pts():
    """Fetch the PTs that failed to process (based on retry logic)."""
    failed_pts = {pt_id: pt_info for pt_id, pt_info in pt_store.items() if pt_info.get("status") == "failed"}
    if not failed_pts:
        return {"message": "No failed PTs."}
    return {"failed_pts": failed_pts}

# Simulate receiving PTs (replace this with your frontend logic)
async def simulate_pt_processing():
    """Simulate receiving PTs to be processed."""
    pt_1 = {
        "pt_id": "pt_001",
        "pt_name": "Portfolio 1",
        "bonds": [
            {"bond_id": "bond_1", "notional": 1000000},
            {"bond_id": "bond_2", "notional": -500000}
        ]
    }
    pt_2 = {
        "pt_id": "pt_002",
        "pt_name": "Portfolio 2",
        "bonds": [
            {"bond_id": "bond_3", "notional": 1500000},
            {"bond_id": "bond_4", "notional": -2000000}
        ]
    }

    await process_new_pt(pt_1)
    await process_new_pt(pt_2)

# To run the simulation in a real environment, you can use this in the main block:
if __name__ == "__main__":
    asyncio.run(simulate_pt_processing())
