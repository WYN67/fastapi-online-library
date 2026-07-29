from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    book_title: str
    book_description: str | None = None
    book_year: int
    book_isbn: str
    book_original_language: str


class BookCreate(BookBase):
    series_id: int | None = None
    author_ids: list[int] = []

class BookResponse(BookBase):
    book_id: int
    model_config = ConfigDict(from_attributes=True)