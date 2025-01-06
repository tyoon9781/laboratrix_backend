from fastapi import APIRouter, Depends, HTTPException, status, Request, Query

from sqlalchemy.orm import Session

from app.schemas import item_schema, token_schema
from app.connect import get_db, redis_client
from app.utils import auth
from app.crud import item_crud
from app.api.auth_api import verify_user_token
from app.api.user_api import verify_user_db
from app.config import CSRF_TOKEN


router = APIRouter(prefix="/items")

async def verify_csrf_token(request: Request, user_token:token_schema.TokenData) -> str:
    form_data = await request.form()
    csrf_token = form_data.get(CSRF_TOKEN)
    if csrf_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No csrftoken")
    
    stored_csrf_token = redis_client.get(user_token.id)
    if stored_csrf_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="csrftoken expired")

    if stored_csrf_token != csrf_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid csrftoken")
    
    return csrf_token


@router.post("/")
def create_item(request: Request, item: item_schema.ItemCreate, db: Session = Depends(get_db)):
    ## verify login token, user exist, csrf token.
    user_token = verify_user_token(request)
    _ = verify_user_db(request)
    _ = verify_csrf_token(user_token)
    redis_client.delete(user_token.id)
    
    return item_crud.create_item(db=db, item=item)

@router.get("/")
def get_items(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="page"),
    size: int = Query(10, ge=1, le=100, description="size"),
):
    db_item = item_crud.get_items(db=db, page=page, size=size)
    return db_item


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.get_item_by_id(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_item

@router.post("/{item_id}")
def update_item(item_id: int, item: item_schema.ItemUpdate, db: Session = Depends(get_db)):
    db_item = item_crud.update_item(
        db=db, item_id=item_id, title=item.title, contents=item.contents
    )
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.delete_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return {"message": "Item deleted"}


@router.post("/{item_id}/comments")
def add_comment(
    item_id: int,
    comment: item_schema.CommentCreate,
    db: Session = Depends(get_db),
    token_data: token_schema.TokenData = Depends(auth.is_valid_token),
):
    db_comment = item_crud.add_comment(
        db=db, contents=comment.contents, item_id=item_id, user_id=token_data.id
    )
    return db_comment


@router.post("/comments/{comment_id}")
def update_comment(
    comment_id: int, comment: item_schema.CommentUpdate, db: Session = Depends(get_db)
):
    db_comment = item_crud.update_comment(
        db=db, comment_id=comment_id, contents=comment.contents
    )
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return db_comment


@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = item_crud.delete_comment(db=db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return {"message": "Comment deleted"}
