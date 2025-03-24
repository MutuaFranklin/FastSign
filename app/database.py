from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create MySQL engine with explicit charset
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # This will log all SQL operations
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={'charset': 'utf8mb4'}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 