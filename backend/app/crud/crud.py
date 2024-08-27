from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models import User, Room, Message, UserRoom
from app.database.schemas import UserCreate, RoomCreate, MessageCreate

class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str):
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def create(self, user: UserCreate):
        db_user = User(username=user.username, hashed_password=user.hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get(self, user_id: int):
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


class RoomCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, room: RoomCreate):
        db_room = Room(name=room.name)
        self.db.add(db_room)
        await self.db.commit()
        await self.db.refresh(db_room)
        return db_room

    async def get(self, room_id: int):
        result = await self.db.execute(select(Room).filter(Room.id == room_id))
        return result.scalars().first()

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(Room).offset(skip).limit(limit))
        return result.scalars().all()

    async def add_user(self, user: User, room: Room):
        user_room = UserRoom(user_id=user.id, room_id=room.id)
        self.db.add(user_room)
        await self.db.commit()
        return user_room


class MessageCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, message: MessageCreate, user_id: int, room_id: int):
        db_message = Message(content=message.content, user_id=user_id, room_id=room_id)
        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def get_by_room(self, room_id: int, skip: int = 0, limit: int = 100):
        result = await self.db.execute(select(Message).filter(Message.room_id == room_id).offset(skip).limit(limit))
        return result.scalars().all()
