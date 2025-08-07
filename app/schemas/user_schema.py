from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GetUserSchema(BaseModel):
    user_id: Optional[int] = None
    user_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    created_on: Optional[datetime] = None
    last_update: Optional[datetime] = None
    is_deleted: Optional[bool] = None


class CreateUserSchema(BaseModel): 
    user_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]


class UpdateUserSchema(BaseModel): 
    user_name: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]


class DeleteUserSchema(BaseModel):
     message : str


class UpdatePasswordSchema(BaseModel):
    password: Optional[str]