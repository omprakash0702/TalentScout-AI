from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
ENV = os.getenv("ENV", "local")

if ENV == "cloud":
    DATABASE_URL = "sqlite:////tmp/test.db"
else:
    DATABASE_URL = "sqlite:///./talentscout.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()