from sqlalchemy.orm import Session
from app.models.item_model import Item, Comment
from app.utils import utc_now


# Item CRUD operations
def create_item(db: Session, title: str, contents: str, user_id: int):
    db_item = Item(title=title, contents=contents, user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, page: int, size: int):
    offset = (page - 1) * size
    return db.query(Item).offset(offset).limit(size).all()


def get_item_by_id(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def update_item(db: Session, item_id: int, title: str, contents: str):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.title = title
        db_item.contents = contents
        db_item.updated_at = utc_now()
        db.commit()
        db.refresh(db_item)
        return db_item
    return None


def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.is_deleted = True
        db_item.deleted_at = utc_now()
        db.commit()
        return db_item
    return None


# Comment CRUD operations
def add_comment(db: Session, contents: str, item_id: int, user_id: int):
    db_comment = Comment(contents=contents, item_id=item_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: int, contents: str):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.contents = contents
        db_comment.updated_at = utc_now()
        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.is_deleted = True
        db_comment.deleted_at = utc_now()
        db.commit()
        return db_comment
    return None
