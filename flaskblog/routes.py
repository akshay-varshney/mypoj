import secrets
import os
from PIL import Image
from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm, updateAccountForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user,login_required
posts=[
    {
        'author': 'Akshay Varshney',
        'title': 'Blog-post-1',
        'Content': 'First Post Content',
        'date_posted' : 'July 15, 2020'

    },
    {
        'author': 'Ridhi Jain',
        'title': 'Blog-post-2',
        'Content': 'Second Post Content',
        'date_posted' : 'July 10, 2020'

    },

]

# Routes are decorators. It will handle all the complicated stuff in the backened and allows us to parse function and return
#the value in the form of the function that will be shown in the website for this specific route.
# '/' is the root page of our website we can thisnk as of the home page and we are simply returning the text for this route.
@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register',methods=['GET','POST']) # to add the functionality to accept the data from the website
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password= bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hashing the passord of the user and then inserting into the DB
        user=User(username=form.username.data, email=form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has sucessfully created and You are able to login now.', 'success')
        return redirect (url_for('Login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login',methods=['GET','POST'])
def Login():
    if current_user.is_authenticated: #if the user is succesfully authenticated then after click it would redirect to home
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember=form.remember.data)
            next_page= request.args.get('next') #If the url contain the next keyword
            return redirect(next_page) if next_page else redirect(url_for('home')) #terniary condition in python  
        else:
            flash('login unsucessfull. Please check email and password', 'danger')
    return render_template('Login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex= secrets.token_hex(8)
    _,f_ext= os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path= os.path.join(app.root_path, 'static/profile_pics',picture_fn)
    output_size=(125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form= updateAccountForm()
    if form.validate_on_submit(): #if the detilas entered are correct and the form and email not already taken then we'll update the values in the database
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file= picture_file
        current_user.username= form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash('Your Account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method== 'GET':
        form.username.data= current_user.username
        form.email.data= current_user. email
    #Adding the default image in the Account Routes
    image_file=url_for('static', filename='profile_pics/'+ 'current_user.image_file') 

    return render_template('account.html', title='Account',image_file=image_file, form=form) 




