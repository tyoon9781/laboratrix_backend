from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils import utc_now, auth


def get_users(db: Session, page: int = 1, size: int = 10):
    return db.query(User).offset((page - 1) * size).limit(size).all()


# User CRUD operations
def create_user(db: Session, email: str, user_name: str, hashed_password: str):
    db_user = User(email=email, user_name=user_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, password: str, is_active: bool):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.hashed_password = password
        db_user.is_active = is_active
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def authenticate_user(db: Session, user_email: str, password: str) -> User|None:
    db_user = db.query(User).filter(User.email == user_email).first()
    
    if db_user is None:
        return None
    
    if not auth.verify_password(password, db_user.hashed_password):
        return None
    
    return db_user