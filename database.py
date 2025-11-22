import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read DB values from .env
DATABASE_USERNAME = os.getenv("DB_USER")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DATABASE_HOSTNAME = os.getenv("DB_HOST")
DATABASE_NAME = os.getenv("DB_NAME")
DATABASE_PORT = os.getenv("DB_PORT", "5432")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
