from sqlalchemy import text
from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from app.connect import get_db, get_redis
import redis

router = APIRouter()


@router.get("/")
def local_root():
    return "hello local"


@router.get("/db_connect")
def connect_db(db=Depends(get_db)):
    try:
        # 임시 쿼리로 데이터베이스 연결 확인 (예: 테이블 목록 조회)
        db.execute(text("SELECT 1"))  # 간단한 SQL 쿼리 실행
        return {"message": "DB connection successful"}
    except SQLAlchemyError as e:
        return {"error": f"DB connection failed: {str(e)}"}


@router.get("/redis_connect")
def connect_redis(redis_client=Depends(get_redis)):
    try:
        # Redis 연결 확인 (ping 테스트)
        redis_client.ping()  # Redis 서버에 ping을 보냄
        return {"message": "Redis connection successful"}
    except redis.exceptions.ConnectionError as e:
        return {"error": f"Redis connection failed: {str(e)}"}
