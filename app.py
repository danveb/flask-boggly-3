"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post 

app = Flask(__name__)
# createdb blogly -> need to create database; \c blogly
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'chickenzarecool123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# define route for users
@app.route('/')
def home_page():
    """Show home page of users"""
    return redirect('/users')

@app.route('/users')
def list_users():
    # instance of user 
    users = User.query.all()
    return render_template('users/users.html', users=users)

@app.route('/users/new')
def new_user_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    """Create new user"""
    # form data 
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    # create new instance 
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url or None)
    # add/commit to database
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info about current user"""
    # throw 404 error if ID not found 
    user = User.query.get_or_404(user_id)
    return render_template('users/details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show form to edit user details"""
    # throw 404 error if ID not found 
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def post_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"]) 
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# POST Routes 

@app.route('/users/<int:user_id>/posts/new') 
def new_post_form(user_id):
    user = User.query.get_or_404(user_id) 
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"]) 
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    
    # form data 
    title = request.form['title']
    content = request.form['content']

    # instance 
    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit() 

    return redirect(f'/users/{user.id}')

@app.route('/posts/<int:post_id>') 
def show_post(post_id):
    post = Post.query.get_or_404(post_id) 
    return render_template('posts/details.html', post=post)

@app.route('/posts/<int:post_id>/edit') 
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_form(post_id): 
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit() 

    return redirect (f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"]) 
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect (f'/users/{post.user_id}')