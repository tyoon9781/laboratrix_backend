import os

## =========================
## Environments
## =========================
LOCAL = "LOCAL"
DEV = "DEV"
PRD = "PRD"
ENV = os.getenv("ENV", LOCAL)
print(f"{ENV=}")


## =========================
## AUTHORIZATION
## =========================
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
LOGIN_SESSION_EXPIRED_MINUTES: int = 60
LOGIN_SESSION_EXPIRED_SECONDS: int = LOGIN_SESSION_EXPIRED_MINUTES * 60
CSRF_TOKEN_EXPIRED_SECONDS = 3600
if None in [SECRET_KEY, ALGORITHM]:
    raise ValueError("Authorization Environments variables are invalid")

CSRF_TOKEN_EXPIRED_SECONDS: int = 3600

## =========================
## Requirements Environments.
## =========================
## local Backend app port
if ENV == LOCAL:
    LOCAL_BACKEND_PORT = os.getenv("BACKEND_CONTAINER_PORT")
    if None in [LOCAL_BACKEND_PORT]:
        raise ValueError("BACKEND Environments variables are invalid")

    LOCAL_BACKEND_PORT = int(LOCAL_BACKEND_PORT)


## =========================
## Database
## =========================
DB_URL = os.getenv("DB_URL")
if ENV == LOCAL:
    DB_TYPE = os.getenv("DB_TYPE")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_CONTAINER_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    if None in [DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]:
        raise ValueError("DB Environments variables are not invalid")

    DB_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    if None in [DB_URL]:
        raise ValueError("DB Environments variables are invalid")


## =========================
## Redis
## =========================
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_HOST_PORT")

if None in [REDIS_HOST, REDIS_PASSWORD, REDIS_PORT]:
    raise ValueError("Redis Environmens variables are invalid")

REDIS_PORT = int(REDIS_PORT)


## =========================
## Information
## =========================
UTF_8 = "utf-8"
ACCESS_TOKEN = "access_token"
CSRF_TOKEN = "csrftoken"
X_CSRF_TOKEN = "X-CSRF-TOKEN"
