from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

username = 'postgres'
password = 'Al-khayr@2002!'
host = 'localhost'
database = 'fastapi'

# Encode the password with @ symbol
encoded_password = quote_plus(password)

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}/{database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()