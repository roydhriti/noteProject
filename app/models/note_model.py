from app.db.base import Base
from sqlalchemy import Column, String, Integer , DateTime, Text, ForeignKey, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship
# from app.models.user_model import UserModel

class NoteModel(Base):
    __tablename__ = 'notes'

    note_id = Column(Integer, primary_key=True, autoincrement=True)
    note_title = Column(String(255), nullable=True)
    note_content = Column(Text, nullable=True)
    created_on = Column(DateTime , default=datetime.utcnow)
    last_update = Column(DateTime , default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.user_id"))


    user = relationship("UserModel", back_populates="notes")