from fastapi import FastAPI, HTTPException
import json
import pyodbc
import os

app = FastAPI()

# Global variable to hold the DB connection
conn = None

def load_sysaccount_secret(secret_path: str = '/vault/secrets/Sysaccount.json'):
    """Load system account credentials from JSON."""
    if not os.path.exists(secret_path):
        raise FileNotFoundError(f"Secret file not found at {secret_path}")
    
    with open(secret_path, 'r') as f:
        sysaccount_data = json.load(f)
    
    return sysaccount_data['username'], sysaccount_data['password']

def create_db_connection(username: str, password: str):
    """Create and return a pyodbc DB connection."""
    try:
        connection = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER=localhost;"  # Adjust to your server
            f"DATABASE=my_database;"  # Adjust to your database
            f"UID={username};"
            f"PWD={password};"
        )
        return connection
    except Exception as e:
        raise Exception(f"Failed to connect to DB: {e}")

@app.on_event("startup")
async def startup_event():
    """Load credentials and create DB connection on app startup."""
    global conn
    try:
        username, password = load_sysaccount_secret()
        conn = create_db_connection(username, password)
        print("Database connection established successfully!")
    except Exception as e:
        print(f"Startup error: {e}")

@app.get("/test-db")
async def test_db():
    """Simple endpoint to test DB connection."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        return {"result": row[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
