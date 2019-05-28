from flask import Blueprint,render_template, url_for, flash, redirect, request
from datetime import datetime, timedelta
from digiLib import webapp, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from digiLib.models import Users,Books,BorrowBook,Cart
from digiLib.controller.users.forms import RegistrationForm
from digiLib.controller.librarians.forms import LoginForm,UpdateAccountForm,RequestResetForm,ResetPasswordForm
from digiLib.controller.librarians.utils import save_picture
from digiLib.controller.users.utils import func_to_borrow

users = Blueprint('users',__name__)

@users.route("/")
@users.route("/home")
def home():
    return render_template('home.html')

@users.route("/logout")
def logout():
    logout_user()
    flash('Logout Sucessfully', 'warning')
    return redirect(url_for('users.home'))

#   Showing Books for User
@users.route('/User/home/showbooks')
def showBooks():
    page = request.args.get('page',1,type=int)
    posts = Books.query.paginate(page=page,per_page=4)
    return render_template('showbooks.html',posts=posts,title='Book-List')

@users.route("/User/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        typeofAcc = 'User'
        user = Users(first_name=form.first_name.data,last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,door_no=form.door_no.data,
            street_name=form.street_name.data,area_name=form.area_name.data,
            country=form.country.data,state=form.state.data,
            postal_code=form.postal_code.data,mobile_number=form.mobile_number.data,
            typeofmembership=form.typeofmembership.data,
            username=form.username.data, email=form.email.data, password=hashed_password,
            security = form.security.data,Account_type=typeofAcc)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/User/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data,Account_type='User').first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home')),flash('Login Successful!', 'success')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/User/account", methods=['GET', 'POST'])
@login_required
def account():
    renewList,returnList = [],[]
    form = UpdateAccountForm()
    posts = BorrowBook.query.filter_by(username=current_user.username).all()
    if len(posts) == 0:flag = 1
    else:flag =0
    if request.method == 'POST':
        if request.form['submit'] == 'Add To Return List':
            print('Add to return List',len(posts));
            flash('Book Added to Return List', 'success')
            return redirect(url_for('users.account'))
        elif request.form['submit'] == 'Add To Renew List':
            print('Book Added to Renew List')
            flash('Book Added to Renew List', 'success')
            return redirect(url_for('users.home'))
        elif request.form['submit'] == 'Return All':
            print('Returning all Books',posts);
            flash('All Books Returned Sucessfully!', 'success')
            for i in range(len(posts)):
                post_book = Books.query.filter_by(book_name=posts[i].book_name,author_name=posts[i].author_name).first()
                post_book.no_of_copies+=1
                db.session.commit()
                db.session.delete(posts[i])
                db.session.commit()            
            return redirect(url_for('users.home'))
        elif request.form['submit'] == 'Renew All':
            print('Returning all Books')
            for i in range(len(posts)):
                post_book = Books.query.filter_by(book_name=posts[i].book_name,author_name=posts[i].author_name).first()
                post_book.no_of_copies+=1
                db.session.commit()
                posts[i].renew_time =datetime.now()+timedelta(minutes = 5)
                db.session.commit()
                print(posts[i].renew_time)
            flash('All Books Renewed Sucessfully!', 'success')
            return redirect(url_for('users.account'))

        if form.validate_on_submit():
            if form.picture.data:
                print(form.picture.data)
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form,posts=posts,flag=flag)


#Route Display Book for Users
@users.route('/User/home/showBooks/<int:book_id>/<flag>',methods=['GET','POST'])
def bookSingle(book_id,flag):
    post = Books.query.get_or_404(book_id);print(flag)
    print(post.isbn_number)
    if request.method == 'POST':
        if request.form['submit'] == 'Borrow':
            func_to_borrow(post,current_user)
            flash('Borrowed Books Sucessfully', 'success')
        elif request.form['submit'] == 'Add to Cart':
            print('We nailed it!')
            add_to_cart = Cart(book_name=post.book_name,author_name=post.author_name,
                book_dept=post.book_dept,isbn_number=post.isbn_number,image_file=post.image_file,
                username=current_user.username,typeofmembership=current_user.typeofmembership,
                no_of_copies=post.no_of_copies,first_name=current_user.first_name)
            db.session.add(add_to_cart)
            db.session.commit()
            flash('Added to Cart', 'success')
    return render_template('book.html',title = post.book_name,post = post,flag=flag)

#   Route for Cart List for Users
@users.route('/User/home/<usernam>/cart',methods=['GET','POST'])
def cartList(usernam):
    posts = Cart.query.filter_by(username=usernam).all()
    if len(posts) == 0:flag = 1
    else:flag =0
    if request.method == 'POST':
        if request.form['submit'] == 'Borrow':
            print('Borrow');
            for i in range(len(posts)):
                func_to_borrow(posts[i],current_user)
                db.session.delete(posts[i]);
                db.session.commit()
            flash('Borrowed Books Sucessfully', 'success')
    return render_template('cart.html',title='Cart',posts=posts,flag=flag)



@users.route('/User/forgot_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        flash('An e-mail has been sent with instructions to reset the password.','info')
        print(token,type(user.username))
        return redirect(url_for('users.reset_password',username=user.username))
    return render_template('reset_request.html',title='Reset Password',form = form)

@users.route('/User/forgot_password/<username>',methods=['GET','POST'])
def reset_password(username):
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users.query.filter_by(username = username).first()
        print(user.password)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',title='Reset Password',form = form)
