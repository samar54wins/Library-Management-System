from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Check if the environment variables are loaded correctly
DATABASE_URL_Docker = os.getenv("DATABASE_URL_Docker")
DATABASE_URL_Local = os.getenv("DATABASE_URL_Local")


def is_docker():
    # Check if Docker is present (based on the existence of /.dockerenv file)
    return os.path.exists("/.dockerenv")

def get_database_url():
    if is_docker():
        DATABASE_URL = DATABASE_URL_Docker
    else:
        DATABASE_URL = DATABASE_URL_Local
    
    print(f"Using database URL: {DATABASE_URL}")  # Debugging line
    return DATABASE_URL

# Usage example
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
