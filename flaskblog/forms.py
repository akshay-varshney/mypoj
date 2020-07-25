from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField 
from flask_wtf.file import FileField, FileAllowed # This is added to upload the image in the Account form. FileFiled is going to be the type of the filed it is while the FileAllowed would be the just like a Validator
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=2,max=15)])
    email= StringField('email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Sign up')

    def validate_username(self,username):
        user= User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is already taken. Please choose another one')

    def validate_email(self,email):
        user= User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is already taken. Please choose another one')
        

class LoginForm(FlaskForm):
    email= StringField('email', validators=[DataRequired(), Email()])
    password= PasswordField('Password', validators=[DataRequired()])
    remember= BooleanField('Remember Me')
    submit= SubmitField('Login')

class updateAccountForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=2,max=15)])
    email= StringField('email', validators=[DataRequired(), Email()])
    picture= FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit= SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username :
            user= User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That Username is already taken. Please choose another one')

    def validate_email(self,email):
        if email.data != current_user.email:
            user= User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is already taken. Please choose another one')
