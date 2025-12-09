import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_router, notes_router
from .websocket_mgr import manager
from .auth import get_current_user
import json

app = FastAPI(title="NoteSync Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(notes_router.router)

# WebSocket endpoint for realtime note editing
@app.websocket("/ws/notes/{note_id}")
async def websocket_note_endpoint(websocket: WebSocket, note_id: str, token: str = None):
    """
    Connect with: ws://host/ws/notes/{note_id}?token=<jwt>
    Messages expected/used:
      - {"type": "edit", "content": "...", "user_id": "..."}
      - {"type": "cursor", "pos": 123}
    """
    # optional token validation (simple)
    try:
        if token:
            # validate token by decoding via dependency
            await get_current_user(token)
    except Exception:
        await websocket.close(code=4401)
        return

    await manager.connect(note_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except Exception:
                continue
            # Broadcast whatever changes to others
            await manager.broadcast(note_id, msg)
    except WebSocketDisconnect:
        manager.disconnect(note_id, websocket)
    except Exception:
        manager.disconnect(note_id, websocket)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
