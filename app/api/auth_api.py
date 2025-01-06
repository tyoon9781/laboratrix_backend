from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import user_schema, token_schema
from app.connect import get_db, redis_client
from app.crud import user_crud
from app.utils import auth
from app.config import LOGIN_SESSION_EXPIRED_SECONDS, ACCESS_TOKEN, CSRF_TOKEN, CSRF_TOKEN_EXPIRED_SECONDS
from app.api.user_api import verify_user_db


router = APIRouter(prefix="/auth")


def verify_user_token(request: Request) -> token_schema.TokenData:
    user_cookie = request.cookies.get(ACCESS_TOKEN)
    if user_cookie is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Token")
    
    user_token = auth.is_valid_token(user_cookie)
    if user_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return user_token


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
async def read_me(request:Request, db: Session = Depends(get_db)):
    user_token = verify_user_token(request)
    db_user = verify_user_db(user_token, db=db)
    return user_schema.UserSend(id=db_user.id, email=db_user.email, user_name=db_user.user_name)

@router.get("/csrftoken", response_model=token_schema.CSRFToken)
async def get_csrftoken(request: Request):
    user_token = verify_user_token(request)
    csrf_token = auth.gen_csrftoken()
    redis_client.set(
        name=user_token.id,
        value=csrf_token,
        ex=CSRF_TOKEN_EXPIRED_SECONDS
    )

    return token_schema.CSRFToken(id=csrf_token)