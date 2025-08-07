from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GetNoteSchema(BaseModel):
    note_id: Optional[int] = None
    user_id: Optional[int] = None
    note_title: Optional[str] = None
    note_content: Optional[str] = None
    created_on: Optional[datetime] = None
    last_update: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    class Config:
        orm_mode = True 
        from_attributes = True



class CreateNoteSchema(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True 
        from_attributes = True



class UpdateNoteSchema(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]

    class Config:
        orm_mode = True 
        from_attributes = True


class DeleteNoteSchema(BaseModel):
    message : str

    
    
class Config:
    orm_mode = True 
    from_attributes = True