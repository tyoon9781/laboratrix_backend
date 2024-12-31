from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import user_schema
from app.connect import get_db
from app.crud import user_crud


router = APIRouter(prefix="/users")


@router.get("/")
def get_users(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    users = user_crud.get_users(db, page, size)
    return users


@router.post("/")
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(
        db=db, email=user.email, user_name=user.user_name, hashed_password=user.password
    )
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
def update_user(user_id: int, user: user_schema.UserUpdate, db: Session = Depends(get_db)):
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

