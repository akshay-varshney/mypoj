from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#app variable setting this to instance of flask class. __name__ is the special module in python that will just the name of the module.
#__name__ is basically calling the main function
# we ahve instantiated flask application in this app variable.
app = Flask(__name__) 
app.config['SECRET_KEY']='7454cba3e9eec9552da080640d876153'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view = 'Login' #After the user not login and go to the account page then in this case it will redirect to the Login page
login_manager.login_message_category= 'info' # To change the message for the login and it is equal to the bootstrap class
from flaskblog import routes
