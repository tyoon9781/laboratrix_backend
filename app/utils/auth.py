import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import crud
from app.connect import get_db
from app.config import SECRET_KEY, ALGORITHM


# OAuth2PasswordBearer는 HTTP에서 토큰을 받아오기 위해 사용합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# JWT에서 사용자 정보를 추출하는 함수
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        # JWT를 디코딩해서 사용자 정보 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # "sub"에 사용자 ID가 담겨 있다고 가정
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        # DB에서 사용자 정보 가져오기
        user = crud.get_user_by_id(db, user_id=user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
