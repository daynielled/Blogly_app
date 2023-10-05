"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']  = 'dgomekey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route('/')
def index():
    """Redirects to list of users"""
    return redirect ("/users")

@app.route('/users')
def list_users():
    """Show all users"""
    users = User.query.all()
    return render_template('users_list.html', title= 'Users List', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Show the add user form"""
    return render_template('add_user.html')

@app.route('user/new', methods=['POST'])
def add_user():
    """Add new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url', 'DEFAULT_PROFILE']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def view_user(user_id):
    """View a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('view_user.html', title='User Detail', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user and return to user list"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form.get('first_name')
        user.last_name = request.form.get('last_name')
        user.image_url = request.form.get('image_url', 'DEFAULT_PROFILE') 

        db.session.add(user)
        db.session.commit()

        return redirect('/users')
    
    return render_template('edit_user.html', title='Edit User', user=user)  

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle delete form submission"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')