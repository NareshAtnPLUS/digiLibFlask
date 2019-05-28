from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from digiLib.models import Users


class RegistrationForm(FlaskForm):
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
    typeofmembership = RadioField('Plans :', choices=[('classic', 'g Classic'), ('standard', 'g $tandard'), ('Prime', 'g Prime')])
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
        user = Users.query.filter_by(username=username.data, Account_type='User').first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data, Account_type='User').first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
