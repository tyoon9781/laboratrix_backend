from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.schemas import token_schema, user_schema
from app.crud import user_crud
from app.utils import auth
from app.connect import get_db, redis_client
from app.config import (
    LOGIN_SESSION_EXPIRED_SECONDS,
    ACCESS_TOKEN,
    CSRF_TOKEN_EXPIRED_SECONDS,
)


router = APIRouter(prefix="/auth")


def verify_user_db(
    user_token: token_schema.TokenData, db: Session = Depends(get_db)
) -> user_schema.User:
    db_user = user_crud.get_user_by_id(db=db, user_id=user_token.id)
    if not db_user or db_user.user_name != user_token.name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No user")
    return db_user


def verify_user_token(request: Request) -> token_schema.TokenData:
    user_cookie = request.cookies.get(ACCESS_TOKEN)
    if not user_cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token")

    user_token = auth.is_valid_token(user_cookie)
    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    return user_token


async def verify_csrf_token(request: Request, body_csrf_token: str) -> str:
    header_csrf_token = request.headers.get("X-CSRF-TOKEN")
    if not body_csrf_token == header_csrf_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid csrf token"
        )
    return body_csrf_token


async def verify_stored_csrf_token(user_token: token_schema.TokenData, csrf_token: str):
    stored_csrf_token = redis_client.get(user_token.id)
    if not stored_csrf_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="csrf token expired"
        )
    if stored_csrf_token != csrf_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid form request"
        )
    redis_client.delete(user_token.id)


@router.get("/me", response_model=user_schema.UserSend)
async def read_me(request: Request, db: Session = Depends(get_db)):
    user_token = verify_user_token(request)
    db_user = verify_user_db(user_token, db)
    return user_schema.UserSend(
        id=db_user.id, email=db_user.email, user_name=db_user.user_name
    )


@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_crud.authenticate_user(
        db=db, user_email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(user)
    response.set_cookie(
        key=ACCESS_TOKEN,
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=LOGIN_SESSION_EXPIRED_SECONDS,
    )
    return token_schema.Token(access_token=access_token, token_type="bearer")


@router.delete("/token")
async def delete_token(response: Response, request: Request):
    request_data: dict = await request.json()
    cookies_to_delete = request_data.get("cookies", [])
    for cookie in cookies_to_delete:
        response.delete_cookie(key=cookie, httponly=True, secure=False, samesite="lax")
    return Response(status_code=status.HTTP_200_OK, headers=response.headers)


@router.get("/csrftoken", response_model=token_schema.CSRFToken)
async def get_csrf_token(request: Request):
    user_token = verify_user_token(request)
    csrf_token = auth.generate_csrf_token()

    redis_client.set(
        name=user_token.id,
        value=csrf_token,
        ex=CSRF_TOKEN_EXPIRED_SECONDS,
    )

    return token_schema.CSRFToken(id=csrf_token)
