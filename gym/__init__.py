from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from gym.config import Config
from flask_pymongo import PyMongo
from boto.s3.connection import S3Connection
import os

try: 
    MONGODB= S3Connection(os.environ['MONGODB'])
except: 
    MONGODB= os.environ['MONGODB']

db = SQLAlchemy()
mongo = PyMongo()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['MONGO_DBNAME'] = 'cloudfitness'
    app.config['MONGO_URI'] = MONGODB
    mongo.init_app(app)
    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from gym.users.routes import users
    app.register_blueprint(users)

    from gym.posts.routes import posts
    app.register_blueprint(posts)

    from gym.main.routes import main
    app.register_blueprint(main)

    # from gym.search.routes import search
    # app.register_blueprint(search)

    from gym.errors.handlers import errors
    app.register_blueprint(errors)


    return app