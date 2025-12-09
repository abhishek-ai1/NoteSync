from typing import Dict, List
from fastapi import WebSocket
import json
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        # note_id -> list of websockets
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, note_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[note_id].append(websocket)

    def disconnect(self, note_id: str, websocket: WebSocket):
        if websocket in self.active_connections[note_id]:
            self.active_connections[note_id].remove(websocket)
        if not self.active_connections[note_id]:
            del self.active_connections[note_id]

    async def broadcast(self, note_id: str, message: dict):
        conns = list(self.active_connections.get(note_id, []))
        if not conns:
            return
        text = json.dumps(message)
        for conn in conns:
            try:
                await conn.send_text(text)
            except Exception:
                # ignore broken connections; cleanup elsewhere
                pass

manager = ConnectionManager()
