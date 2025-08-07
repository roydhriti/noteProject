from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.models.user_model import UserModel
from app.schemas.note_schema import CreateNoteSchema, UpdateNoteSchema, DeleteNoteSchema
from app.services.note_service import get_all_note, create_note, update_note,delete_note


router = APIRouter()


@router.get("/", response_model=dict)
def read_notes_endpoint(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_all_note(db, current_user)


@router.post("/", response_model=dict, status_code=201)
def create_new_note_endpoint(
    note_data: CreateNoteSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return create_note(db, note_data, current_user)


@router.put("/{note_id}", response_model=dict)
def update_existing_note_endpoint(
    note_id: int,
    note_data: UpdateNoteSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return update_note(db, note_id, note_data, current_user)


@router.delete("/{note_id}", response_model=DeleteNoteSchema)
def soft_delete_note_endpoint(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    delete_note(db, note_id)
    return {"message" : "User deleted successfully",}