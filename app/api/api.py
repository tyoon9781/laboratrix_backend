# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError
# from app import crud, schemas, auth
# from app.connect import get_db, get_redis
# from app.config import ENV, LOCAL
# import redis


# router = APIRouter()


# ## local connection test api
# if ENV == LOCAL:
#     from sqlalchemy import text

#     @router.get("/local/")
#     def local_root():
#         return "hello local"

#     @router.get("/local/db_connect")
#     def connect_db(db=Depends(get_db)):
#         try:
#             # 임시 쿼리로 데이터베이스 연결 확인 (예: 테이블 목록 조회)
#             db.execute(text("SELECT 1"))  # 간단한 SQL 쿼리 실행
#             return {"message": "DB connection successful"}
#         except SQLAlchemyError as e:
#             return {"error": f"DB connection failed: {str(e)}"}

#     @router.get("/local/redis_connect")
#     def connect_redis(redis_client=Depends(get_redis)):
#         try:
#             # Redis 연결 확인 (ping 테스트)
#             redis_client.ping()  # Redis 서버에 ping을 보냄
#             return {"message": "Redis connection successful"}
#         except redis.exceptions.ConnectionError as e:
#             return {"error": f"Redis connection failed: {str(e)}"}


# @router.get("/users")
# def get_users(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
#     users = crud.get_users(db, page, size)
#     return users


# @router.post("/users")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.create_user(
#         db=db, email=user.email, user_name=user.user_name, hashed_password=user.password
#     )
#     return db_user


# @router.get("/users/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db=db, user_id=user_id)
#     if not db_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     return db_user


# @router.post("/users/{user_id}")
# def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud.update_user(
#         db=db, user_id=user_id, password=user.password, is_active=user.is_active
#     )
#     if not db_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     return db_user


# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_id(db=db, user_id=user_id)
#     if not db_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
#         )
#     db_user.is_deleted = True
#     db.commit()
#     return {"message": "User deleted"}


# @router.post("/items")
# def create_item(
#     item: schemas.ItemCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(auth.get_current_user),
# ):
#     db_item = crud.create_item(
#         db=db, title=item.title, contents=item.contents, user_id=current_user["id"]
#     )
#     return db_item


# @router.get("/items/{item_id}")
# def get_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = crud.get_item_by_id(db=db, item_id=item_id)
#     if not db_item:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
#         )
#     return db_item


# @router.post("/items/{item_id}")
# def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
#     db_item = crud.update_item(
#         db=db, item_id=item_id, title=item.title, contents=item.contents
#     )
#     if not db_item:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
#         )
#     return db_item


# @router.delete("/items/{item_id}")
# def delete_item(item_id: int, db: Session = Depends(get_db)):
#     db_item = crud.delete_item(db=db, item_id=item_id)
#     if not db_item:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
#         )
#     return {"message": "Item deleted"}


# @router.post("/items/{item_id}/comments")
# def add_comment(
#     item_id: int,
#     comment: schemas.CommentCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(auth.get_current_user),
# ):
#     db_comment = crud.add_comment(
#         db=db, contents=comment.contents, item_id=item_id, user_id=current_user["id"]
#     )
#     return db_comment


# @router.post("/items/comments/{comment_id}")
# def update_comment(
#     comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)
# ):
#     db_comment = crud.update_comment(
#         db=db, comment_id=comment_id, contents=comment.contents
#     )
#     if not db_comment:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
#         )
#     return db_comment


# @router.delete("/items/comments/{comment_id}")
# def delete_comment(comment_id: int, db: Session = Depends(get_db)):
#     db_comment = crud.delete_comment(db=db, comment_id=comment_id)
#     if not db_comment:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
#         )
#     return {"message": "Comment deleted"}
