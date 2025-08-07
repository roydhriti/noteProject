from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI Project",
    description="A simple FastAPI project with Swagger UI",
    version="1.0.0"
)

# Request schema
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with Swagger!"}


# Swagger UI is available at: http://localhost:8000/docs
# ReDoc UI is available at: http://localhost:8000/redoc
