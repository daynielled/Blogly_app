"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

DEFAULT_PROFILE = "https://www.pngitem.com/pimgs/m/361-3619033_person-icon-one-person-icon-blue-hd-png.png"



class User(db.Model):
    """ Site user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, nullable=False, default= DEFAULT_PROFILE)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

@property    
def get_full_name(self):
    """ Return full name of user """
    return f"{self.first_name} {self.last_name}"
     

class Post(db.Model):
    """Blog Posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@property
def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    """Tag on a post"""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


    
class Tag(db.Model):
    """Tags that can be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(40), nullable = False, unique = True)

    posts = db.relationship('Post',secondary="posts_tags", backref="tags")


def connect_db(app):
    """Conect the database to the flask app"""
    db.app = app
    db.init_app(app)