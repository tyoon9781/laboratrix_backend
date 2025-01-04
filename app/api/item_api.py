from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas import item_schema, token_schema
from app.connect import get_db
from app.utils import auth
from app.crud import item_crud

router = APIRouter()


@router.get("/items")
def get_items(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="page"),
    size: int = Query(10, ge=1, le=100, description="size"),
):
    db_item = item_crud.get_items(db=db, page=page, size=size)
    return db_item


@router.post("/items")
def create_item(
    item: item_schema.ItemCreate,
    db: Session = Depends(get_db),
    token_data: token_schema.TokenData = Depends(auth.is_valid_token),
):
    db_item = create_item(
        db=db, title=item.title, contents=item.contents, user_id=token_data.id
    )
    return db_item


@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.get_item_by_id(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_item


@router.post("/items/{item_id}")
def update_item(
    item_id: int, item: item_schema.ItemUpdate, db: Session = Depends(get_db)
):
    db_item = item_crud.update_item(
        db=db, item_id=item_id, title=item.title, contents=item.contents
    )
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return db_item


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = item_crud.delete_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return {"message": "Item deleted"}


@router.post("/items/{item_id}/comments")
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


@router.post("/items/comments/{comment_id}")
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


@router.delete("/items/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = item_crud.delete_comment(db=db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return {"message": "Comment deleted"}
