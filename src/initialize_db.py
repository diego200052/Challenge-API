# initialize_db.py
from core.database import engine, Base

# Create all tables for first time
Base.metadata.create_all(bind=engine)
