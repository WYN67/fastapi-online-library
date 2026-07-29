from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse
from app.services.book import BookService


router = APIRouter()


@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    found_book = await service.get_book_by_isbn(book_data.book_isbn)
    if found_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"A book with ISBN {book_data.book_isbn} already exists")
    return await service.create_book(book_data)


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_one_book(book_id: int, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    found_book = await service.get_book_by_id(book_id)
    if not found_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return found_book


@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    deleting_book = await service.delete_book(book_id)
    if not deleting_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
