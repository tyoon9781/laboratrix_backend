from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.utils import utc_now
from app.connect import Base


class User(Base):
    ## 실제 DB table name
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    user_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    deleted_at = Column(DateTime, nullable=True)

    ## 외부와 연관된 부분. 순환참조를 피하기 위해 string으로 class, attribute를 입력한다.
    items = relationship("Item", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
