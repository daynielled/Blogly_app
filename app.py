"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
# from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY']  = 'dgomezkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()



@app.route('/')
def index():
    """Show recent posts"""
    posts= Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return render_template('homepage_post.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    """Show 404 NOT FOUND page."""

    return render_template('404.html'), 404

#######User Routes########

@app.route('/users')
def list_users():
    """Show info on all users"""
    users = User.query.order_by (User.last_name, User.first_name).all()
    return render_template('users_list.html', users=users)


@app.route('/users/new', methods=['GET'])
def new_user_form():
    """Show the add user form"""
    return render_template('add_user.html')


@app.route('/user/new', methods=['POST'])
def add_user():
    """ Handle form submission for adding new user"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url', 'DEFAULT_PROFILE']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    
    db.session.add(new_user)
    db.session.commit()
    flash(f"User {new_user.get_full_name} added! ")
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def view_user(user_id):
    """View info on a specific user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts.all()

    return render_template('view_user.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show a form to edit user """
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html',user=user)  

     
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edited_user(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url', 'DEFAULT_PROFILE']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.get_full_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Handle delete form submission"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.get_full_name} has been deleted.")

    return redirect('/users')

#######Post Routes#########

@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    """Show form to add a post for that user"""

    user = User.query.get_or_404(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_posts(user_id):
    """Handle form submission for a new post and redirect to the user detail page"""

    user = User.query.get_or_404(user_id)
    title = request.form.get['title']
    content = request.form.get['content']

    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post.title}" added')

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show a post.Show buttons to edit and delete the post """
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_posts_form(post_id):
    """Show form to edit a post and to cancel(back to the post page)"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_posts(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title= request.form['title']
    post.content= request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f'/users/{post.user_id}')


