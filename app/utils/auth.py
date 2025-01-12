from fastapi.security import OAuth2PasswordBearer
from app.config import LOGIN_SESSION_EXPIRED_SECONDS, SECRET_KEY, ALGORITHM, UTF_8
from app.schemas.user_schema import User
from app.schemas.token_schema import TokenData

import uuid
import jwt
import bcrypt
import time


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")


def generate_csrftoken() -> str:
    return uuid.uuid4().hex


def _peppered_password(plain_password: str) -> str:
    return plain_password + SECRET_KEY


def gen_hashed_password(plain_password: str) -> str:
    peppered_password_bytes = _peppered_password(plain_password).encode(UTF_8)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(peppered_password_bytes, salt)
    return hashed.decode(UTF_8)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered_password_bytes = _peppered_password(plain_password).encode(UTF_8)
    hashed_bytes = hashed_password.encode(UTF_8)
    return bcrypt.checkpw(peppered_password_bytes, hashed_bytes)


def create_access_token(user: User):
    iat = int(time.time())
    exp = iat + LOGIN_SESSION_EXPIRED_SECONDS
    data = TokenData(id=user.id, name=user.user_name, iat=iat, exp=exp)

    to_encode = data.model_dump()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def is_valid_token(token_str: str) -> TokenData | None:
    try:
        token_dict = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**token_dict)
    except Exception as e:
        return None

    if token_data.exp < time.time():
        return None

    return token_data
