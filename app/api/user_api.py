from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import user_schema, token_schema
from app.connect import get_db
from app.crud import user_crud
from app.utils import auth
from app.config import LOGIN_SESSION_EXPIRED_SECONDS, ACCESS_TOKEN, CSRF_TOKEN
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

@router.post("/token", response_model=token_schema.TokenData)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db=db, user_email=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="[ERROR] Incorrect username or password",
            headers={"WWW-Authneticate": "Bearer"}
        )
    access_token = auth.create_access_token(user)
    response.set_cookie(
        key=ACCESS_TOKEN, value=access_token, httponly=True, secure=False,
        max_age=LOGIN_SESSION_EXPIRED_SECONDS)
    return token_schema.TokenData(access_token=access_token, token_type="bearer")

@router.delete("/token")
async def logout(response: Response):    
    cookies_to_delete = [ACCESS_TOKEN, CSRF_TOKEN]
    for cookie in cookies_to_delete:
        response.delete_cookie(key=cookie, httponly=True, secure=False)
    return Response(status_code=status.HTTP_200_OK, headers=response.headers)

@router.get("/me")
async def get_me(request:Request, db: Session = Depends(get_db)):
    token_str = request.cookies.get(ACCESS_TOKEN)
    if token_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="[ERROR] No token."
        )
    
    token_data = auth.is_valid_token(token_str)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="[ERROR] token is invalid."
        )
    user = user_crud.get_user_by_id(db=db, user_id=token_data.id)
    if user is None or token_data.name != user.user_name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="[ERROR] token is invalid."
        )
    
    return user_schema.userSend(id=user.id, email=user.email, user_name=user.user_name)

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

