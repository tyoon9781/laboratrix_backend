from fastapi import FastAPI
from app.api import item_api, user_api, local_api
from app.config import ENV, LOCAL
from app.connect import local_create_tables


app = FastAPI()

app.include_router(item_api.router, prefix="/api")
app.include_router(user_api.router, prefix="/api")

if ENV == LOCAL:
    # local 전용 api
    app.include_router(local_api.router, prefix="/api")
    app.add_event_handler("startup", local_create_tables)
