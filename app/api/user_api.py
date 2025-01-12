from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import user_schema, token_schema
from app.connect import get_db
from app.crud import user_crud
from app.utils import auth
from app.config import LOGIN_SESSION_EXPIRED_SECONDS, ACCESS_TOKEN, CSRF_TOKEN

router = APIRouter(prefix="/users")


def verify_user_db(
    user_token: token_schema.TokenData, db: Session = Depends(get_db)
) -> user_schema.User:
    db_user = user_crud.get_user_by_id(db=db, user_id=user_token.id)
    if db_user is None or db_user.user_name != user_token.name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return db_user


@router.get("/")
def get_users(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, page, size)
    return users


@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = user_crud.create_user(db=db, user_create=user)
    return db_user


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.post("/{user_id}")
def update_user(
    user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)
):
    db_user = user_crud.update_user(
        db=db, user_id=user_id, password=user.password, is_active=user.is_active
    )
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    db_user.is_deleted = True
    db.commit()
    return {"message": "User deleted"}
