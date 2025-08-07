from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.auth import get_current_user
from app.models.user_model import UserModel
from app.services.user_service import get_user_by_id, register_user, update_user, update_password, delete_user
from app.schemas.user_schema import CreateUserSchema, UpdateUserSchema, UpdatePasswordSchema, DeleteUserSchema
from app.utils.password import verify_password
from app.utils.jwt import create_access_token
from datetime import timedelta
from app.core.config import settings


router = APIRouter()


@router.get("/me")
def get_user_endpoint(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_by_id(db, current_user)

@router.post("/register")
def register_user_endpoint(register_data: CreateUserSchema, db: Session = Depends(get_db)):
    return register_user(db, register_data)


@router.put("/{user_id}")
def update_user_endpoint(
    user_id: int,
    update_data: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can't update another user")
    return update_user(db, user_id, update_data)


@router.delete("/{user_id}", response_model=DeleteUserSchema)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can't delete another user")
    
    delete_user(db, user_id)

    return {"message" : "User deleted successfully",}


@router.put("/{user_id}/password")
def update_password_endpoint(
    user_id: int,
    password_data: UpdatePasswordSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can't change another user's password")
    return update_password(db, user_id, password_data)



@router.post("/login", status_code=200)
def login( email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user or (user.is_deleted):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account does not exist. Please create a new account."
        )

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )

    me = user

    return {"access_token": access_token, "token_type": "bearer","me": me}
