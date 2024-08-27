# app/websockets/chat.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import MessageCRUD, RoomCRUD
from app.database import get_db
from app.auth.auth import AuthService

chat_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@chat_router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: AsyncSession = Depends(get_db), auth_service: AuthService = Depends()):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            user = await auth_service.get_current_user(websocket.headers.get('Authorization'), db)
            message_crud = MessageCRUD(db)
            await message_crud.create(data, user.id, room_id)
            await manager.broadcast(f"User {user.username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {user.username} left the chat")
