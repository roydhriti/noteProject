from fastapi import APIRouter
from app.routers import user_router

routes = APIRouter()

routes.include_router(user_router.router, prefix="/users", tags=["Users"])