from sqlalchemy import Column, Float, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base=declarative_base()


class User_Credentials(Base):
    __tablename__='user_data'
    
    user_name=Column(String , primary_key=True, nullable=False)
    password=Column(String,nullable=False)
    
    
    
class book(Base):
    __tablename__='books'
    
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String,nullable=False)
    author=Column(String,nullable=False)
    genre=Column(String,nullable=False)
    published_year=Column(Integer,nullable=False)
    reviews = relationship("Review", back_populates="r_book", cascade="all, delete-orphan")
    
    
class Review(Base):
    __tablename__="reviews"
    id = Column(Integer, primary_key=True,autoincrement=True)
    review=Column(String,nullable=False)
    book_id=Column(Integer,ForeignKey('books.id', ondelete="CASCADE"),nullable=False)
    r_book=relationship("book",back_populates="reviews")
    
    

# class Review(Base):
#     __tablename__ = "reviews"
    
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     review = Column(String, nullable=False)
#     book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"), nullable=False)
#     user = Column(String, ForeignKey('user_data.user_name'), nullable=False)
#     book = relationship("book", back_populates="reviews")
#     user_details = relationship("User_Credentials", back_populates="reviews")
