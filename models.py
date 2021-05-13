"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy() 
DEFAULT_IMG_URL = "https://cdn.vox-cdn.com/thumbor/G_w4Nyo9IJx5q5xa5E92vJCVyUQ=/21x0:539x345/1200x800/filters:focal(21x0:539x345)/cdn.vox-cdn.com/assets/3727699/Dogecoin_logo.png"

def connect_db(app):
    db.app = app
    db.init_app(app) 

# Models 
class User(db.Model):
    """User Model"""
    __tablename__ = 'users' 

    # define columns 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    # need relationship between post and user 
    # ON DELETE CASCADE 
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

class Post(db.Model):
    """Post Model"""
    __tablename__ = 'posts' 

    # columns 
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)