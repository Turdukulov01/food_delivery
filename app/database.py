from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Используем синхронное подключение для теста
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Nurdan1224@localhost:5432/food_delivery"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
