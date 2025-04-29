from fastapi import FastAPI, HTTPException
import json
import pyodbc
import os

app = FastAPI()

# Global variables
username = None
password = None

def load_sysaccount_secret(secret_path: str = '/vault/secrets/Sysaccount.json'):
    """Load system account credentials from JSON."""
    if not os.path.exists(secret_path):
        raise FileNotFoundError(f"Secret file not found at {secret_path}")
    
    with open(secret_path, 'r') as f:
        sysaccount_data = json.load(f)
    
    return sysaccount_data['username'], sysaccount_data['password']

def create_db_connection(username: str, password: str):
    """Create and return a pyodbc DB connection."""
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={Settings().db_server};"
        f"DATABASE={Settings().db_database};"
        f"UID={username};"
        f"PWD={password};"
    )
    return connection

class Settings:
    """Configuration settings using simple class (we will make this pydantic soon)."""
    def __init__(self):
        self.secret_path = os.getenv("SECRET_PATH", "/vault/secrets/Sysaccount.json")
        self.db_server = os.getenv("DB_SERVER", "localhost")
        self.db_database = os.getenv("DB_DATABASE", "my_database")

@app.on_event("startup")
async def startup_event():
    """Load credentials on app startup."""
    global username, password
    try:
        username, password = load_sysaccount_secret(Settings().secret_path)
        print("Loaded system account credentials.")
    except Exception as e:
        print(f"Startup error: {e}")

@app.get("/test-db")
async def test_db():
    """Simple endpoint to test DB connection."""
    try:
        connection = create_db_connection(username, password)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        row = cursor.fetchone()
        connection.close()
        return {"result": row[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


#Pydantic settings

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuration using Pydantic BaseSettings."""
    secret_path: str = "/vault/secrets/Sysaccount.json"
    db_server: str = "localhost"
    db_database: str = "my_database"

    class Config:
        env_file = ".env" 
