from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session

from app.schemas import item_schema
from app.connect import get_db, redis_client
from app.crud import item_crud
from app.api.auth_api import (
    verify_user_token,
    verify_user_db,
    verify_csrf_token,
    verify_stored_csrf_token,
)

router = APIRouter(prefix="/items")


@router.post("/", response_model=item_schema.Item)
async def create_item(
    request: Request,
    input_item: item_schema.ItemCreateRequest,
    db: Session = Depends(get_db),
):
    user_token = verify_user_token(request)
    verify_user_db(user_token, db)
    csrf_token = await verify_csrf_token(request, input_item.csrf_token)
    await verify_stored_csrf_token(user_token, csrf_token)

    item = item_schema.ItemCreate(
        user_id=user_token.id,
        title=input_item.title,
        contents=input_item.contents,
    )
    return item_crud.create_item(db=db, item=item)


@router.get("/", response_model=item_schema.ItemView)
def read_items(
    currPage: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    skip = (currPage - 1) * size
    items = item_crud.get_items(db, skip=skip, limit=size)
    count = item_crud.get_items_count(db)
    return {"items": items, "count": count}


@router.get("/{item_id}", response_model=item_schema.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = item_crud.get_item_by_id(db=db, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/{item_id}/comments", response_model=item_schema.Comment)
async def create_comment(
    request: Request,
    item_id: int,
    comment: item_schema.CommentCreate,
    db: Session = Depends(get_db),
):
    user_token = verify_user_token(request)
    verify_user_db(user_token, db)
    return item_crud.create_comment(
        db=db, comment=comment, user_id=user_token.id, item_id=item_id
    )


@router.get("/{item_id}/comments", response_model=list[item_schema.Comment])
def read_comments(
    item_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    comments = item_crud.get_comments_by_item_id(
        db=db, item_id=item_id, skip=skip, limit=limit
    )
    return comments
