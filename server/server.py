import asyncio
import websockets
import json

# Dummy data with five columns: ID, Name, Category, Quantity, and Price
data = [
    {"id": 1, "name": "Item A", "category": "Category 1", "quantity": 10, "price": 100.0},
    {"id": 2, "name": "Item B", "category": "Category 2", "quantity": 5, "price": 200.0},
    {"id": 3, "name": "Item C", "category": "Category 3", "quantity": 8, "price": 150.0},
    {"id": 4, "name": "Item D", "category": "Category 1", "quantity": 12, "price": 300.0},
    {"id": 5, "name": "Item E", "category": "Category 2", "quantity": 7, "price": 250.0},
]

connected_clients = set()

async def send_data(websocket):
    """Send the current data to a newly connected client."""
    await websocket.send(json.dumps(data))

async def notify_clients():
    """Notify all connected clients about the updated data."""
    if connected_clients:  # Check if there's at least one connected client
        message = json.dumps(data)
        await asyncio.wait([client.send(message) for client in connected_clients])

async def handle_client(websocket, path):
    """Handle incoming WebSocket connections."""
    # Register the new client
    connected_clients.add(websocket)
    try:
        # Send initial data to the client
        await send_data(websocket)

        async for message in websocket:
            # Parse the received data
            received_data = json.loads(message)

            # Update the corresponding row in the dummy data
            for item in data:
                if item["id"] == received_data["id"]:
                    item.update(received_data)
                    break

            # Notify all clients about the updated data
            await notify_clients()

    finally:
        # Unregister the client on disconnect
        connected_clients.remove(websocket)

async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "localhost", 6789):
        print("WebSocket server started at ws://localhost:6789")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())