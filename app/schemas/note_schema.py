from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class GetNoteSchema(BaseModel):
    note_id: Optional[int] = None
    note_title: Optional[str] = None
    note_content: Optional[str] = None
    created_on: Optional[datetime] = None
    last_update: Optional[datetime] = None
    is_deleted: Optional[bool] = None


class CreateNoteSchema(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]


class UpdateNoteSchema(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]
    created_on: Optional[datetime]
    last_update: Optional[datetime]

class DeleteNoteSchema(BaseModel):
     message : str