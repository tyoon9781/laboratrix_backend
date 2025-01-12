from fastapi import FastAPI
from app.api import item_api, user_api, auth_api
from app.config import ENV, LOCAL


app = FastAPI()

api_prefix = "/api"

app.include_router(auth_api.router, prefix=api_prefix)
app.include_router(item_api.router, prefix=api_prefix)
app.include_router(user_api.router, prefix=api_prefix)

if ENV == LOCAL:
    from app.connect import Base, engine, SessionLocal
    from app.crud import user_crud
    from app.utils import auth
    from app.api import local_api

    def make_table():
        Base.metadata.create_all(bind=engine)

    def create_admin_user():
        db = SessionLocal()
        admin_email = "admin@example.com"
        admin_name = "admin"
        hashed_password = auth.gen_hashed_password("qwer1234")
        admin_user = user_crud.get_user_by_email(db, email=admin_email)
        if admin_user is None:
            print("Admin is not exist. create new one.")
            user_crud.create_user(db=db, email=admin_email, user_name=admin_name, hashed_password=hashed_password)
        else:
            print("Admin is exist")
        db.close()

    # local 전용 api
    app.include_router(local_api.router)
    app.add_event_handler("startup", make_table)
    app.add_event_handler("startup", create_admin_user)
