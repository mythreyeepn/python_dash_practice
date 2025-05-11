
import asyncio
from typing import Dict, List

class InMemoryPubSubManager:
    def __init__(self):
        self.subscribers: Dict[str, List] = {}

    def register(self, channel: str, websocket):
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        if websocket not in self.subscribers[channel]:
            self.subscribers[channel].append(websocket)

    def unregister(self, channel: str, websocket):
        if channel in self.subscribers:
            if websocket in self.subscribers[channel]:
                self.subscribers[channel].remove(websocket)
            if not self.subscribers[channel]:
                del self.subscribers[channel]

    async def publish(self, channel: str, message: dict):
        if channel in self.subscribers:
            for websocket in self.subscribers[channel]:
                try:
                    await websocket.send_json(message)
                except Exception:
                    continue  # skip dead connections

    def get_active_channels(self):
        return list(self.subscribers.keys())
