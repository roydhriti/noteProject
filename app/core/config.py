import os
from pydantic_settings import BaseSettings
from pathlib import Path


# Get the absolute path of the .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / f".env"

class Settings(BaseSettings):
    app_name: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int


    class Config:
        env_file = str(ENV_FILE)
        extra = "allow"

settings = Settings()
