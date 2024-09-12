"""Blogly application."""

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


app.config['SECRET_KEY'] = "SECRET"
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def all_users():
    """Home page that shows a list of all users. With a 'Add user' button."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users.html", users=users)


@app.route('/users/new')
def create_user_form():
    """Show create a user form."""
    return render_template("create.html")


@app.route('/users/new', methods=["POST"])
def create_user():
    """Create a new user and add them to the database."""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    img_url = request.form["img_url"] or None
    # if not (img_url):
    #     img_url = None
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show details about a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_detail_form(user_id):
    """Show the edit page for a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_detail(user_id):
    """Save the edited details of a single user."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["img_url"] or None
    # if not (img_url):
    #     img_url = None
    # user.image_url = img_url
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user_from_db(user_id):
    """Delete a single user from the database."""
    # user = User.query.get_or_404(user_id)
    User.delete_by_id(user_id)
    db.session.commit()
    return redirect("/users")
