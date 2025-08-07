from fastapi import APIRouter
from app.routers import user_router, note_router

routes = APIRouter()

routes.include_router(user_router.router, prefix="/users", tags=["Users"])
routes.include_router(note_router.router, prefix="/notes", tags=["Notes"])
