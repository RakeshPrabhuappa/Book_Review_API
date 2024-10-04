import os
import datetime
import jwt
from fastapi import Depends, FastAPI, HTTPException
from models import Base, User_Credentials, book, Review
from authorization import get_header, remove_bearer
from connection import session 
from schema import User_Details, Book_Details, update_book, Review_book, BookSearchRequest
from dotenv import load_dotenv
from hash import hash_password, verify_password

load_dotenv()
secret_key=os.getenv("SECRET_KEY")


app=FastAPI()



@app.post("/sign_up")
async def user_sign_up(item: User_Details):
    try:
        username = item.user_name
        password = item.pswrd
        
        hsh_pass = hash_password(password)

        # Check if the username already exists in the database
        check_username = session.query(User_Credentials).filter(User_Credentials.user_name == username).first()

        if check_username:
            return ("User name already exists")
        else:
            add_user = User_Credentials(user_name=username, password=hsh_pass)
            
            session.add(add_user)
            session.commit()
            
            session.close()
            
            return ("User added successfully")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/user_login")
async def user_login(item: User_Details):
    try:
        username = item.user_name
        password = item.pswrd
        
        # Prepare payload for JWT token, including username and expiration time
        payload = {
            "user_name": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        
        check_username = session.query(User_Credentials).filter(User_Credentials.user_name == username).first()
        
        if check_username and verify_password(password, check_username.password):       
            # Generate a JWT token upon successful login
            encode_token = jwt.encode(payload, secret_key, algorithm="HS256")              
            return ("Login successful.......Your Token for adding books is:", encode_token)
        else:
            return ("Invalid username or password")
        
    except Exception as e:
        return ("error in user_login", e)

        
        
@app.post("/add_books")
async def add_books(item: Book_Details, token_username: str = Depends(get_header)):
    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is invalid")
    
    title = item.book_title
    author = item.book_author
    genre = item.book_genre
    published_year = item.book_published
    
    user = session.query(User_Credentials).filter(User_Credentials.user_name == token_username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    add_bk = book(title=title, author=author, genre=genre, published_year=published_year)
    
    session.add(add_bk)
    
    session.commit()
    
    return f"Thank you {user.user_name} for adding Book"

    
    
    
@app.patch("/update_books/{id}")
async def updating_books(id: int, item: update_book, token_username: str = Depends(get_header)):
    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is Invalid")
    
    user = session.query(User_Credentials).filter(User_Credentials.user_name == token_username).first()
    
    if user:
        search_book_id = session.query(book).filter(book.id == id).first()
        
        if not search_book_id:
            raise HTTPException(status_code=401, detail="Enter a valid book Id")

        title = item.book_title
        author = item.book_author
        genre = item.book_genre
        published_year = item.book_published
        
        if title is not None:
            search_book_id.title = title          
        if author is not None:
            search_book_id.author = author        
        if genre is not None:
            search_book_id.genre = genre          
        if published_year is not None:
            search_book_id.published_year = published_year     
        session.commit()
        
        return f"Message: Thank you {user.user_name} for updating Book"
    else:
        raise HTTPException(status_code=401, detail="User not found")

        
        
@app.delete("/delete_books/{delete_id}")
async def delete_book(delete_id: int, token_username: str = Depends(get_header)):
    try:
        if delete_id not in book.id:
            raise HTTPException(status_code=404, detail="Book not found")
    except TypeError as e:
        return e

    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is Invalid")
    
    user = session.query(User_Credentials).filter(User_Credentials.user_name == token_username).first()
     
    if user:
        search_id = session.query(book).filter(book.id == delete_id).first()
        
        if not search_id:
            raise HTTPException(status_code=401, detail=f"{user.user_name} : Please Enter a valid id")
        
        session.delete(search_id)
        session.commit()  
        
        return f"Message: {user.user_name} selected id:{search_id.id} has been deleted"
    else:
        raise HTTPException(status_code=401, detail="Invalid username")



@app.get("/view_books/")
async def get_books(token_username:str=Depends(get_header)):
    try:
        if not token_username:
            raise HTTPException(status_code=401,detail="Given Token is Invalid")
        
        user=session.query(User_Credentials).filter(User_Credentials.user_name==token_username).first()
        if user:
            view_book=session.query(book).order_by(book.id).all()
            
            if view_book is None:
                raise HTTPException(status_code=401,detail="Book is empty")
            result={}
            for index,b in enumerate(view_book):
                result[f"book{index + 1}"] =b.title
            return f"Books :{result}"
    except Exception as e:
        return ("Error in view books",e)
        
            
      
@app.post("/post_review")
async def post_review(item: Review_book, token_username: str = Depends(get_header)):
    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is Invalid")

    user = session.query(User_Credentials).filter(User_Credentials.user_name == token_username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    review_content = item.review_content
    review_book_id = item.review_book_id
    
    view_book = session.query(book).filter(book.id == review_book_id).first()
    if not view_book:
        raise HTTPException(status_code=404, detail="Book ID not found")

    try:
        add_review = Review(review=review_content, book_id=review_book_id)
        session.add(add_review)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error in posting review")

    return {f"message : Thanks {user.user_name} for posting review"}

            
                      
@app.get("/view_review/{disp_review}")
async def view_review(disp_review:str,token_username: str = Depends(get_header)):
    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is Invalid")

    user = session.query(User_Credentials).filter(User_Credentials.user_name == token_username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    user_review=session.query(Review).join(book).filter(book.title==disp_review).first()
    if not user_review:
        raise HTTPException(status_code=401, detail="Book not found")
    return user_review

            

@app.get("/advance_search")
async def view_review_book(
    search_request: BookSearchRequest,  
    token_username: str = Depends(get_header)  
):
    if not token_username:
        raise HTTPException(status_code=401, detail="Given Token is Invalid")

    try:
        query = session.query(book)  

        if search_request.b_id is not None:
            query = query.filter(book.id == search_request.b_id)  

        if search_request.b_title is not None:
            query = query.filter(book.title == search_request.b_title)  

        if search_request.b_author is not None:
            query = query.filter(book.author == search_request.b_author)  

        if search_request.b_genre is not None:
            query = query.filter(book.genre == search_request.b_genre)  

        results = query.all()

        if not results:
            raise HTTPException(status_code=404, detail="No books found matching the criteria")

        formatted_results = {}
        
        for index, bk in enumerate(results):
            formatted_results[f"book{index + 1}"] = bk  

        return formatted_results

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
