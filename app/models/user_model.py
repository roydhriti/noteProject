from app.db.base import Base
from sqlalchemy import Column, String, Integer , DateTime
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_on = Column(DateTime , default=datetime.utcnow)
    last_update = Column(DateTime , default=datetime.utcnow)
