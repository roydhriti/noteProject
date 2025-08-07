from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user_model import UserModel
from app.models.note_model import NoteModel
from fastapi import HTTPException, status
from app.schemas.note_schema import GetNoteSchema, CreateNoteSchema, UpdateNoteSchema

def get_all_note(db: Session, current_user: UserModel):
    getNote = db.query(NoteModel).filter(NoteModel.user_id == current_user.user_id, NoteModel.is_deleted == False).all()

    if not getNote:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return {
        "message": "Note retrieved successfully",
        "note": getNote
    }


def create_note(db: Session, createNote_data: CreateNoteSchema, current_user: UserModel):
    
    try:

        user_dict = createNote_data.dict(exclude_unset=True)
        user_dict["created_on"] = datetime.utcnow()
        user_dict["user_id"] = current_user.user_id

        new_note = NoteModel(**user_dict)
    
        db.add(new_note)
        db.commit()
        db.refresh(new_note)

        note_schema = GetNoteSchema.from_orm(new_note)

            
        return {
            "message": "Note Created successfully",
            "new_note": note_schema
        }
    
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=400, detail=f"Error creating note: {str(e)}")


def update_note(
    db: Session, note_id: int, updateNote_data: UpdateNoteSchema, current_user: UserModel
):    
    try:
        get_existing_note = db.query(NoteModel).filter(
            NoteModel.note_id == note_id, NoteModel.is_deleted == False
        ).first()

        if not get_existing_note:            
            raise HTTPException(status_code=404, detail="User not found")


        update_data = updateNote_data.dict(exclude_unset=True)
        update_data["last_update"] = datetime.utcnow()
        update_data["user_id"] = current_user.user_id

        for key, value in update_data.items():
            
            setattr(get_existing_note, key, value)

        db.commit()
        db.refresh(get_existing_note)

        note_schema = GetNoteSchema.from_orm(get_existing_note)

        return {
        "message": "Note updated successfully",
        "update_note": note_schema
        }

    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error updating note: {str(e)}")


def delete_note(db: Session, note_id: int):
    deleted_note = db.query(NoteModel).filter(NoteModel.note_id == note_id, NoteModel.is_deleted == False).first()
    
    if not deleted_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found or already deleted"
            )
        
    deleted_note.is_deleted = True 


    db.commit()  
    db.refresh(deleted_note) 
    
    return deleted_note

