import os
from pydantic_settings import BaseSettings
from pathlib import Path

# Determine the environment (default is 'local')
ENV = os.getenv("ENVIRONMENT", "local")

# Get the absolute path of the .env file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / f".env.{ENV}"

class Settings(BaseSettings):
    app_name: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    email_host_user: str 
    email_host_password: str 
    domain_url: str
    email_smtp_server: str
    email_smtp_port: int
    GOOGLE_CLIENT_ID: str 

    class Config:
        env_file = str(ENV_FILE)
        extra = "allow"

settings = Settings()
