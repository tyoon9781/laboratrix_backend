import os


## Environments
LOCAL = "LOCAL"
DEV = "DEV"
PRD = "PRD"
ENV = os.getenv("ENV", LOCAL)
print(f"{ENV=}")


## AUTHORIZATION
## CAUTION : Don't use dummy secret key in server environment.
SECRET_KEY = os.getenv("SECRET_KEY")
if None in [SECRET_KEY]:
    if ENV != LOCAL:
        raise ValueError("SECRET_KEY is not invalid")
    else:
        SECRET_KEY = (
            "dummy_secret_key_jjr673rnvq9fqrqnks7le+uo=4#k_s87x9q$p+l4qk=8yit*#6"
        )

ALGORITHM = os.getenv("ALGORITHM", "HS256")


## Requirements Environments.
## local Backend app port
LOCAL_BACKEND_PORT = os.getenv("BACKEND_CONTAINER_PORT")
if None in [LOCAL_BACKEND_PORT]:
    raise ValueError("BACKEND Environments variables are not invalid")

LOCAL_BACKEND_PORT = int(LOCAL_BACKEND_PORT)


## Database
DB_TYPE = os.getenv("DB_TYPE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_CONTAINER_PORT") if ENV == LOCAL else os.getenv("DB_HOST_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if None in [DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]:
    raise ValueError("DB Environments variables are not invalid")

DB_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


## Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_PORT = os.getenv("REDIS_HOST_PORT")

if None in [REDIS_HOST, REDIS_PASSWORD, REDIS_PORT]:
    raise ValueError("Redis Environmens variables are not invalid")

REDIS_PORT = int(REDIS_PORT)
