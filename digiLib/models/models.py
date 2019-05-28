from datetime import datetime,timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from digiLib import db, login_manager, webapp
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20),nullable=False)    
    last_name = db.Column(db.String(20),nullable=False)
    date_of_birth = db.Column(db.String(10),nullable=False)
    door_no = db.Column(db.String(3),nullable=False)    
    street_name = db.Column(db.String(70),nullable=False)
    area_name = db.Column(db.String(20),nullable=False)
    country = db.Column(db.String(20),nullable=False)
    state = db.Column(db.String(20),nullable=False)
    postal_code = db.Column(db.String(7),nullable=False)
    mobile_number = db.Column(db.String(14),nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    typeofmembership = db.Column(db.String(20),nullable=False,default='LibrarianAccount')
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    security = db.Column(db.String(20),nullable=False)
    Account_type = db.Column(db.String(20),nullable = False)


    def get_reset_token(self,expires_sec = 1800):
        s = Serializer(webapp.config['SECRET_KEY'],expires_sec)
        return s.dumps({str(id):self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(user_id):
        s = Serializer(webapp.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    '''def __init__(self,first_name,last_name,date_of_birth,door_no,street_name,
                    area_name,country,state,postal_code,mobile_number,username,email,
                    image_file):
                    self.first_name = first_name;self.last_name = last_name;self.date_of_birth = date_of_birth;
                    self.door_no = door_no;self.street_name = street_name;self.area_name = area_name;
                    self.country = country;self.state = state;self.postal_code = postal_code;
                    self.mobile_number = mobile_number;self.username = username;self.email = email;
                    self.image_file = image_file'''

'''class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"'''

class Books(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String(100),nullable=False)
    author_name = db.Column(db.String(30),nullable=False)
    book_dept = db.Column(db.String(20),nullable=False)
    book_cost = db.Column(db.String(20),nullable=False)
    book_des = db.Column(db.String(10000),nullable=False)
    year_published = db.Column(db.String(20),nullable=False)
    book_pub = db.Column(db.String(50),nullable=False)
    isbn_number = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultbook.jpg')
    no_of_pages = db.Column(db.Integer,nullable=False)
    no_of_copies = db.Column(db.Integer,nullable=False)
    no_ofCopies = db.Column(db.Integer,nullable=False)
    floor_no = db.Column(db.Integer,nullable=False)
    rack_no = db.Column(db.Integer,nullable=False)
    shelf_no = db.Column(db.Integer,nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    

    '''def __init__(self,book_name,author_name,book_dept,
        book_cost,book_des,year_published,isbn_number,
        image_file,no_of,unique=True_pages,no_of_copies,floor_no,rack_no,shelf_no):
        self.id = id;self.book_name = book_name;self.author_name = author_name
        self.book_dept = book_dept;self.book_cost = book_cost;self.book_des = book_des
        self.year_published = year_published;self.isbn_number = isbn_number;self.image_,unique=Truefile = image_f,unique=Trueile;
        self.no_of_copies = no_of_copies;self.no_of_pages = no_of_pages;self.floor_no = floor_no;
        self.rack_no = rack_no;self.shelf_no = shelf_no'''

class Cart(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    book_name = db.Column(db.String(100),nullable=False)
    author_name = db.Column(db.String(20),unique=True,nullable=False)
    book_dept = db.Column(db.String(20),nullable=False)
    isbn_number = db.Column(db.String(20),unique=True,nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultbook.jpg')
    username = db.Column(db.String(20), nullable=False)
    typeofmembership = db.Column(db.String(20),nullable=False)
    no_of_copies = db.Column(db.Integer,nullable=False)
    first_name = db.Column(db.String(20),nullable=False)

# class Borrow(db.Model,UserMixin):
#     id = db.Column(db.Integer,primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     book_name = db.Column(db.String(20),nullable=False)
#     author_name = db.Column(db.String(20),unique=True,nullable=False)

class Requestion(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    book_name = db.Column(db.String(20),nullable=False)
    author_name = db.Column(db.String(20),unique=True,nullable=False)
    book_dept = db.Column(db.String(20),nullable=False)
    book_implementation = db.Column(db.String(500),nullable=False)

class BorrowBook(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    book_name = db.Column(db.String(100),nullable=False)
    author_name = db.Column(db.String(20),nullable=False)
    book_dept = db.Column(db.String(20),nullable=False)
    isbn_number = db.Column(db.String(20),unique=True,nullable=False)
    borrow_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    renew_time = db.Column(db.DateTime, nullable=False, default=datetime.now()+timedelta(minutes=5))
    image_file = db.Column(db.String(20), nullable=False, default='defaultbook.jpg')
    fine = db.Column(db.Integer,nullable=False,default=0)

class Country(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    alpha_2 = db.Column(db.String(5),nullable=False)
    alpha_3 = db.Column(db.String(5),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    numeric = db.Column(db.String(10),nullable=False)
    official_name = db.Column(db.String(100),nullable=True)
