from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from digiLib.models import Users


class RegistrationFormLib(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name: ', validators=[DataRequired(), Length(min=2, max=20)])
    date_of_birth = StringField('Date of Birth: ', validators=[DataRequired(), Length(min=8, max=10)])
    door_no = StringField('Door No: ', validators=[DataRequired(), Length(min=1, max=3)])
    street_name = StringField('Street Name: ', validators=[DataRequired(), Length(min=10, max=70)])
    area_name = StringField('Area/Locality: ', validators=[DataRequired(), Length(min=3, max=20)])
    country = StringField('Country: ', validators=[DataRequired(), Length(min=2, max=20)])
    state = StringField('State: ', validators=[DataRequired(), Length(min=3, max=20)])
    postal_code = StringField('Postal Code: ', validators=[DataRequired(), Length(min=6, max=7)])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=14)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    security = StringField("Enter Your First Company You've Joined: ", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data, Account_type='Librarian').first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data, Account_type='Librarian').first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

#       Form for Registering Books
class AddBooks(FlaskForm):
    book_name = StringField('Book Name : ', validators=[DataRequired(), Length(min=3, max=100)])
    author_name = StringField('Author Name : ', validators=[DataRequired(), Length(min=3, max=100)])
    book_dept = StringField('Book Department Name : ', validators=[DataRequired(), Length(min=3, max=30)])
    book_cost = StringField('Cost of book in : ₹. ', validators=[DataRequired(), Length(min=3, max=10)])
    book_des = TextAreaField('Book Description :  ', validators=[DataRequired(), Length(min=3, max=10000)])
    #picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    year_published = StringField('Year Published : ', validators=[DataRequired(), Length(min=4, max=4)])
    book_pub = StringField('Publication : ', validators=[DataRequired(), Length(min=3, max=50)])
    isbn_number = StringField('ISBN Number : ', validators=[DataRequired(), Length(min=9, max=20)])
    no_of_pages = StringField('Number of pages : ', validators=[DataRequired(), Length(min=2, max=4)])
    no_of_copies = IntegerField(' Number of copies', validators=[DataRequired()])
    floor_no = IntegerField('Floor Number : ', validators=[DataRequired()])
    rack_no = IntegerField('Rack Number : ', validators=[DataRequired()])
    shelf_no = IntegerField('Shelf No : ', validators=[DataRequired()])
    submit = SubmitField('Add New Book and Insert Image')


class UpdateImageBook(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Image')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    security = StringField("Enter Your First Company You've Joined: ", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Request Password Reset')

    def validate_user(self, email, security):
        user = User.query.filter_by(email=email.data, security=security.data).first()
        if user is None:
            raise ValidationError('There is no Account with that email.You must Register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')            