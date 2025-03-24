from fastapi import APIRouter, HTTPException
import pyodbc

router = APIRouter()

# Database connection settings
DB_CONFIG = {
    "server": "your_server",
    "database": "your_database",
    "username": "your_username",
    "password": "your_password",
    "driver": "{ODBC Driver 17 for SQL Server}"
}

def get_db_connection():
    """Establish a database connection"""
    conn_str = f"DRIVER={DB_CONFIG['driver']};SERVER={DB_CONFIG['server']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['username']};PWD={DB_CONFIG['password']}"
    return pyodbc.connect(conn_str)

# GET API
@router.get("/items/{item_id}")
async def get_item(item_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Items WHERE id = ?", item_id)
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "name": row[1], "price": row[2]}
        raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POST API
@router.post("/items/")
async def create_item(name: str, price: float):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Items (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        return {"message": "Item created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT API
@router.put("/items/{item_id}")
async def update_item(item_id: int, name: str, price: float):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Items SET name = ?, price = ? WHERE id = ?", (name, price, item_id))
        conn.commit()
        conn.close()
        return {"message": "Item updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    

#     from fastapi import APIRouter
# from app.api.routes import my_api  # Import the new API module

# router = APIRouter()

# router.include_router(my_api.router, prefix="/api", tags=["items"])


# from fastapi import APIRouter
# from app.api.routes import router as routes_router  # Import aggregated routes

# router = APIRouter()
# router.include_router(routes_router, prefix="/api")  # All routes now start with `/api`


# import uvicorn
# from fastapi import FastAPI
# from app.api.api import router as api_router
# from app.core.settings import settings

# def get_application() -> FastAPI:
#     application = FastAPI(title="credit-api-services", debug=settings.debug, version="1.0")

#     # Register API routes
#     application.include_router(api_router, prefix="/api")

#     return application

# app = get_application()

# # ✅ Add this test route below
# @app.get("/")
# async def root():
#     return {"message": "FastAPI is running!"}

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)

