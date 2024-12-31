from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DB_URL, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
import redis


Base = declarative_base()
engine = create_engine(DB_URL, pool_size=100)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def local_create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis():
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,  # Redis에서 반환되는 값이 문자열로 처리되도록 설정
    )
    return client
