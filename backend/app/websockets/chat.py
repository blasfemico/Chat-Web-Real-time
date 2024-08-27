from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.crud.crud import MessageCRUD, RoomCRUD, UserCRUD
from app.database import get_db
from app.auth.auth import AuthService
from app.database.schemas import MessageCreate
from core.exceptions import RoomNotFoundError

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
async def websocket_endpoint(websocket: WebSocket, room_id: int, db: Session = Depends(get_db), auth_service: AuthService = Depends()):
    await manager.connect(websocket)
    try:
        # Autenticar usuario
        token = websocket.cookies.get("Authorization")
        if token is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        current_user = auth_service.get_current_user(db, token=token)

        # Verificar si la sala existe
        room_crud = RoomCRUD(db)
        room = room_crud.get(room_id)
        if room is None:
            raise RoomNotFoundError()

        # Agregar usuario a la sala si no está ya en ella
        room_crud.add_user(current_user, room)

        while True:
            data = await websocket.receive_text()
            message_crud = MessageCRUD(db)
            new_message = message_crud.create(MessageCreate(content=data), user_id=current_user.id, room_id=room_id)
            await manager.broadcast(f"User {current_user.username}: {new_message.content}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User {current_user.username} left the chat")
    except HTTPException as e:
        await websocket.close(code=e.status_code)
