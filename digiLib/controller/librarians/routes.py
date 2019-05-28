from flask import Blueprint,render_template, url_for, flash, redirect, request
from digiLib import webapp, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from digiLib.models import Users,Books
from digiLib.controller.librarians.forms import (RegistrationFormLib,LoginForm,UpdateAccountForm,
                                AddBooks,UpdateImageBook,RequestResetForm,ResetPasswordForm)
from digiLib.controller.librarians.utils import save_picture,save_picture_book

librarians = Blueprint('librarians',__name__)

@librarians.route("/Librarian/loginLib/home")
def homeLib():
    return render_template('home(Librarian).html')    

@librarians.route("/logout")
def logout():
    logout_user()
    flash('Logout Sucessfully', 'warning')
    return redirect(url_for('users.home'))

# Route for Registering Librarians
@librarians.route("/Librarian/registerLib", methods=['GET', 'POST'])
def registerLib():
    if current_user.is_authenticated:
        return redirect(url_for('librarians.homeLib'))
    form = RegistrationFormLib()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        typeofAcc = 'Librarian'
        user = Users(first_name=form.first_name.data,last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,door_no=form.door_no.data,
            street_name=form.street_name.data,area_name=form.area_name.data,
            country=form.country.data,state=form.state.data,
            postal_code=form.postal_code.data,mobile_number=form.mobile_number.data,
            username=form.username.data,email=form.email.data, password=hashed_password,
            security = form.security.data,Account_type=typeofAcc)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('librarians.loginLib'))
    return render_template('registerLib.html', title='Register', form=form)






#Route for Librarians Login
@librarians.route("/Librarian/loginLib", methods=['GET', 'POST'])
def loginLib():
    if current_user.is_authenticated:
        return redirect(url_for('librarians.homeLib'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data,Account_type='Librarian').first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('librarians.homeLib')),flash('Login Successful!', 'success')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginLib.html', title='Login', form=form)


#   Route for Registering New Books
@librarians.route("/Librarian/homeLib/addBooks",methods=['GET','POST'])
@login_required
def addBook():
    form = AddBooks()
    if form.validate_on_submit():
        book = Books(book_name=form.book_name.data,author_name=form.author_name.data,
            book_dept=form.book_dept.data,book_cost=form.book_cost.data,
            book_des=form.book_des.data,book_pub=form.book_pub.data,year_published=form.year_published.data,
            isbn_number=form.isbn_number.data,no_of_pages=form.no_of_pages.data,no_of_copies=form.no_of_copies.data,
            no_ofCopies=form.no_of_copies.data,floor_no=form.floor_no.data,rack_no=form.rack_no.data,shelf_no=form.shelf_no.data)
        db.session.add(book);db.session.commit()
        flash(f'{form.book_name.data} Added into Database successfully!','success')
        return redirect(url_for('librarians.Updatebookinfo',book=form.book_name.data))
    return render_template('addBook.html',title='Register Books',form=form)


@librarians.route("/Librarian/accountLib", methods=['GET', 'POST'])
@login_required
def accountLib():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('librarians.accountLib'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account(Librarians).html', title='Account',
                           image_file=image_file, form=form)



#Routes to Add Image to datebase
@librarians.route('/Librarian/homeLib/addBooks/addImage=<book>',methods=['GET','POST'])
def Updatebookinfo(book):
    form = UpdateImageBook()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_book(form.picture.data)
            print(picture_file,book)
            updat = Books.query.filter_by(book_name=book).first()
            updat.image_file = str(picture_file)
            db.session.commit()
        flash(f'Image Added into Database successfully!','success')
        return redirect(url_for('librarians.homeLib'))
    return render_template('updateimage.html',form=form)


#Routes to Monitor Books for Librarians
@librarians.route('/Librarian/homeLib/MonitorBooks')
@login_required
def MonitorBooks():
    posts = BorrowBook.query.all()
    return render_template('MonitorBooks.html',posts=posts)

#Routes to Borrowed Books for Librarians
@librarians.route('/Librarian/homeLib/BorrowedBooks')
@login_required
def BorrowedBooks():
    return render_template('BorrowedBooks.html')

#Routes to Add Books for Librarians
@librarians.route('/Librarian/homeLib/MonitorStudents')
@login_required
def MonitorStudents():
    return render_template('MonitorStudents.html')
