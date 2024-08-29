from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.database.models import User, Room, Message, UserRoom
from app.database.schemas import UserCreate, RoomCreate, MessageCreate
from typing import Optional

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        db_user = User(username=user.username, hashed_password=self.get_password_hash(user.password))
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_password_hash(self, password: str) -> str:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)


class RoomCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, room: RoomCreate):
        db_room = Room(name=room.name)
        self.db.add(db_room)
        self.db.commit()
        self.db.refresh(db_room)
        return db_room

    def get(self, room_id: int):
        return self.db.query(Room).filter(Room.id == room_id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(Room).offset(skip).limit(limit).all()

    def add_user(self, user: User, room: Room):
        user_room = UserRoom(user_id=user.id, room_id=room.id)
        self.db.add(user_room)
        self.db.commit()
        return user_room


class MessageCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: MessageCreate, user_id: int, room_id: int):
        db_message = Message(content=message.content, user_id=user_id, room_id=room_id)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_by_room(self, room_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(Message).filter(Message.room_id == room_id).offset(skip).limit(limit).all()




# alejandro gay