from app.db.base import Base
from sqlalchemy import Column, String, Integer , DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.note_model import NoteModel

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime , default=datetime.utcnow)
    last_update = Column(DateTime , default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


    notes = relationship("NoteModel", back_populates="user")