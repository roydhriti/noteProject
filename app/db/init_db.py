from app.db.base import Base
from app.db.session import engine

def init_db():
    from app.models import user_model
    
    Base.metadata.create_all(bind=engine)