from sqlalchemy import (Column, Integer, String, Date, ForeignKey, Table, Float,DateTime,Boolean,DECIMAL)
from sqlalchemy.orm import relationship, DeclarativeBase
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SqlEnum
class BaseModel(DeclarativeBase):
    pass



class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)

  
    books = relationship("BookModel", back_populates="user")

    def __repr__(self):
        return f"user {self.username}"


class AuthorModel(BaseModel):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    fullname = Column(String(120), nullable=False)

    
    books = relationship("BookModel", back_populates="author")

    def __repr__(self):
        return f"author {self.fullname}"


class BookModel(BaseModel):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(300))
    author_id = Column(Integer, ForeignKey("authors.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("AuthorModel", back_populates="books")
    user = relationship("UserModel", back_populates="books")

    def __repr__(self):
        return f"book {self.title}"