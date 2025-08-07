from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.user_model import UserModel
from fastapi import HTTPException, status
from app.schemas.user_schema import CreateUserSchema, UpdateUserSchema, UpdatePasswordSchema, DeleteUserSchema
from app.utils.jwt import create_access_token
from app.utils.password import get_password_hash

def get_user_by_id(db: Session, current_user: UserModel):
    getUser = db.query(UserModel).filter(UserModel.user_id == current_user.user_id, UserModel.is_deleted == False).first()

    if not getUser:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "message": "User retrieved successfully",
        "user": getUser
    }


def register_user(db: Session, register_data: CreateUserSchema,):
    
    try:

        existing_user = db.query(UserModel).filter(UserModel.email == register_data.email).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")


        user_dict = register_data.dict(exclude_unset=True)
        user_dict["password"] = get_password_hash(user_dict["password"])
        user_dict["created_on"] = datetime.utcnow()
        new_user = UserModel(**user_dict)
    
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token({"email": new_user.email}, expires_delta=timedelta(hours=1))
            
        return {
            "message": "Registred successfull",
            "new_user": new_user
        }
    
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=400, detail=f"Error creating user: {str(e)}")


def update_user(
    db: Session, user_id: int, updateUser_data: UpdateUserSchema
):    
    try:
        get_existing_user = db.query(UserModel).filter(
            UserModel.user_id == user_id, UserModel.is_deleted == False
        ).first()

        if not get_existing_user:            
            raise HTTPException(status_code=404, detail="User not found")


        update_data = updateUser_data.dict(exclude_unset=True)
        update_data["last_update"] = datetime.utcnow()

        for key, value in update_data.items():
            
            setattr(get_existing_user, key, value)

        db.commit()
        db.refresh(get_existing_user)

        return {
        "message": "User updated successfully",
        "update_user": get_existing_user
        }

    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error updating user: {str(e)}")


def delete_user(db: Session, user_id: int):
    deleted_user = db.query(UserModel).filter(UserModel.user_id == user_id, UserModel.is_deleted == False).first()
    
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or already deleted"
            )
        
    deleted_user.is_deleted = True 


    db.commit()  
    db.refresh(deleted_user) 
    
    return deleted_user


def update_password(db: Session, user_id: int, updatePassword_data: UpdatePasswordSchema):
    try:
        get_existing_user = db.query(UserModel).filter(
            UserModel.user_id == user_id, UserModel.is_deleted == False
        ).first()

        if not get_existing_user:            
            raise HTTPException(status_code=404, detail="User not found")


        update_password = updatePassword_data.dict(exclude_unset=True)
        update_password["last_update"] = datetime.utcnow()

        for key, value in update_password.items():
            
            setattr(get_existing_user, key, value)

        db.commit()
        db.refresh(get_existing_user)

        return {
        "message": "Password updated successfully",
        "update_pass": get_existing_user
        }

    except Exception as e:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Error updating password: {str(e)}")
