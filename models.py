"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_PROFILE = "https://www.pngitem.com/pimgs/m/361-3619033_person-icon-one-person-icon-blue-hd-png.png"



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    middle_name = db.Column(db.String)
    img_url = db.Column(db.Text, nullable=False, default= 'DEFAULT_PROFILE')


def connect_db(app):
    db.app = app
    db.init_app(app)

def get_full_name(self):
     if self.middle_name:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
     else:
        return f"{self.first_name} {self.last_name}"

