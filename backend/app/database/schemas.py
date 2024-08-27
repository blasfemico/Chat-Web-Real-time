from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Room Schemas (Si planeas trabajar con salas de chat)
class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attribute= True

# Message Schemas (Para manejar los mensajes en las salas de chat)
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    timestamp: datetime
    user_id: int
    room_id: int

    class Config:
        from_attribute = True
