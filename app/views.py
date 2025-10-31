from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import *
from .auth import jwt_required
from .models import *
from sqlalchemy.orm import Session
from db_config import get_my_db


api = APIRouter()
    
@api.post("/authors", tags=["Author"])
async def create_author(author_data: AuthorSchema, db: Session = Depends(get_my_db), user=Depends(jwt_required)):
    author = AuthorModel(fullname=author_data.fullname)
    db.add(author)
    db.commit()
    db.refresh(author)
    return {"message": "Author created successfully"}


@api.get("/authors", tags=["Author"])
async def get_authors(db: Session = Depends(get_my_db)):
    authors = db.query(AuthorModel).all()
    return {"authors": authors}


@api.get("/authors/{author_id}", tags=["Author"])
async def get_author(author_id: int, db: Session = Depends(get_my_db)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return {"author": author}


@api.delete("/authors/{author_id}", tags=["Author"])
async def delete_author(author_id: int, db: Session = Depends(get_my_db), user=Depends(jwt_required)):
    author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted successfully"}




@api.post("/books", tags=["Books"])
async def create_book(book_data: BookSchema, db: Session = Depends(get_my_db), user=Depends(jwt_required)):
    author = db.query(AuthorModel).filter(AuthorModel.id == book_data.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book = BookModel(title=book_data.title,description=book_data.description,author_id=book_data.author_id, user_id=book_data.user_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"message": "Book created successfully"}


@api.get("/books", tags=["Books"])
async def get_books(db: Session = Depends(get_my_db)):
    books = db.query(BookModel).all()
    return {"books": books}


@api.get("/books/{book_id}", tags=['Books'])
async def get_book(book_id: int, db: Session = Depends(get_my_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"book": book}


@api.delete("/books/{book_id}", tags=["Books"])
async def delete_book(book_id: int, db: Session = Depends(get_my_db), user=Depends(jwt_required)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}