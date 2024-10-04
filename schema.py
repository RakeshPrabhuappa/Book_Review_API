from pydantic import BaseModel
from typing import Optional

class User_Details(BaseModel):
    user_name:str
    pswrd:str
    
    
class Book_Details(BaseModel):
    id:int | None=None
    book_title:str
    book_author:str
    book_genre:str
    book_published:int
    
    
class update_book(BaseModel):
    book_title:str | None=None
    book_author:str | None=None
    book_genre:str | None=None
    book_published:int | None=None

    
class Review_book(BaseModel):
    id:int | None=None
    review_content:str
    review_book_id:int
    
    
    
class BookSearchRequest(BaseModel):
    b_id: Optional[int] = None
    b_title: Optional[str] = None
    b_author: Optional[str] = None
    b_genre: Optional[str] = None
    