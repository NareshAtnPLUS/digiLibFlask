import os,secrets
from PIL import Image
from datetime import datetime, timedelta
from digiLib import webapp, db
from digiLib.models import BorrowBook,Books

# Function to Borrow
def func_to_borrow(post,current_user):
    if current_user.typeofmembership == 'standard':renewTime = datetime.now()+timedelta(minutes = 5)
    elif current_user.typeofmembership == 'Prime':renewTime = datetime.now()+timedelta(minutes = 10)
    elif current_user.typeofmembership == 'classic':renewTime = datetime.now()+timedelta(minutes = 2)
    bokborrow = BorrowBook(username=current_user.username,book_name=post.book_name,
        author_name=post.author_name,book_dept=post.book_dept,image_file=post.image_file,
        isbn_number=post.isbn_number,renew_time=renewTime)
    db.session.add(bokborrow)
    db.session.commit()
    post_book = Books.query.filter_by(book_name=post.book_name,author_name=post.author_name).first()
    post_book.no_of_copies-=1
    db.session.commit()