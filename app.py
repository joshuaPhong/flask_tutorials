# from flask import Flask, render_template, url_for, flash, redirect, request
# from flask_login import (
#     LoginManager,
#     login_user,
#     logout_user,
#     login_required,
#     current_user,
# )
# from flask_migrate import Migrate
# from forms import RegistrationForm, LoginForm, LogoutForm, CreatePostForm
# from models import db, User, Posts
# from flask_dotenv import DotEnv
#
# app = Flask(__name__)
#
# DotEnv().init_app(app)
# # import Flask class from flask module
# app.config["SECRET_KEY"] = "df9980f341166cf2f58a0167a55a8f6e"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# # app.config["MESSAGE_FLASHING_OPTIONS"] = {"duration": 5}
#
# db.init_app(app)
# with app.app_context():
#     db.create_all()
# # ?create a migration instance
# migrate = Migrate(app, db)
# # ?create a login manager instance
# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = "login"
#
#
# # Creates a user loader callback that returns the user object given an id
# @login_manager.user_loader
# def loader_user(user_id):
#     return User.query.get(user_id)
#
#
# @app.route("/")
# @app.route("/home")
# @login_required
# # define a function for the route, pass in the template file, posts dict,
# # and title
# def home():  # put application's code here
#     user_posts = Posts.query.all()
#     return render_template("home.html", posts=user_posts, title="Home", page="home")
#
#
# # route for individual post
# @app.route("/post/<int:post_id>")
# def post(post_id):
#     post = Posts.query.get_or_404(post_id)
#     return render_template("post.html", title=post.title, post=post)
#
#
# @app.route("/posts")
# def posts():
#     all_posts = Posts.query.all()
#     return render_template("posts.html", title="All Posts", posts=all_posts)
#
#
# @app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
# @login_required
# def update_post(post_id):
#     post = Posts.query.get_or_404(post_id)
#     if post.author != current_user:
#         flash("You are not authorized to update this post", "danger")
#         return redirect(url_for("home"))
#     form = CreatePostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.content = form.content.data
#         db.session.commit()
#         flash("Your post has been updated!", "success")
#         return redirect(url_for("post", post_id=post.id))
#     elif request.method == "GET":
#         form.title.data = post.title
#         form.content.data = post.content
#     return render_template("create_post.html", title="Update Post", form=form)
#
#
# # route for about
# @app.route("/about")
# def about():
#     return render_template("about.html", title="About", page="about")
#
#
# # route for login
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     message = ""
#     # query the database for the user
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         # check if the user exists and the password is correct
#         if user and user.check_password(form.password.data):
#             # use a login function to log the user in
#             login_user(user)
#             message += f"You have been logged in!"
#             flash(message, "success")
#             return redirect(url_for("home"))
#         else:
#             message += f"Login Unsuccessful. Please check email and password"
#             flash(message, "danger")
#     elif form.is_submitted():
#         message += f"Form is invalid"
#         flash(message, "danger")
#     return render_template("login.html", title="Login", page="login", form=form)
#
#
# # route for register
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     form = RegistrationForm()
#     message = ""
#     if form.validate_on_submit():
#
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#         )
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#
#         message += f"Account created for {form.username.data}!" f" {user.username}"
#         flash(message, "success")
#         return redirect(url_for("home"))
#     elif form.is_submitted():
#         message += "Form is invalid"
#         flash(message, "danger")
#     return render_template(
#         "register.html",
#         title="Register",
#         page="register",
#         form=form,
#         message=message,
#     )
#
#
# # route for logout
# @app.route("/logout", methods=["GET", "POST"])
# def logout():
#     form = LogoutForm()
#     message = ""
#     if form.validate_on_submit():
#         logout_user()
#         message += f"You have been logged out!"
#         flash(message, "success")
#         return redirect(url_for("home"))
#     elif form.is_submitted():
#         message += f"Form is invalid"
#         flash(message, "danger")
#     return render_template("logout.html", title="Logout", page="logout", form=form)
#
#
# # route for create_posts
# @app.route("/create_post", methods=["GET", "POST"])
# @login_required
# def create_post():
#     form = CreatePostForm()
#     message = ""
#     if form.validate_on_submit():
#         post = Posts(
#             title=form.title.data, content=form.content.data, user_id=current_user.id
#         )
#         db.session.add(post)
#         db.session.commit()
#         message += f"Post created for {form.title.data}!"
#         flash(message, "success")
#         return redirect(url_for("home"))
#     elif form.is_submitted():
#         message += f"Form is invalid"
#         flash(message, "danger")
#     return render_template(
#         "create_post.html",
#         title="Create Post",
#         page="create_post",
#         form=form,
#     )
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_migrate import Migrate
from forms import (
    RegistrationForm,
    LoginForm,
    LogoutForm,
    CreatePostForm,
    UpdateProfileForm,
)
from models import db, User, Posts
from flask_dotenv import DotEnv

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from a .env file
DotEnv().init_app(app)

# Set the secret key for session management
app.config["SECRET_KEY"] = "df9980f341166cf2f58a0167a55a8f6e"

# Set the database URI for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Initialize the database with the app
db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize Flask-Login for user session management
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


# User loader callback for Flask-Login
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


# Route for the home page
@app.route("/")
@app.route("/home")
@login_required
def home():
    # Query all posts from the database
    user_posts = Posts.query.all()
    # Render the home template with the posts
    return render_template("home.html", posts=user_posts, title="Home", page="home")


# Route for the about page
@app.route("/about")
def about():
    # Render the about template
    return render_template("about.html", title="About", page="about")


# Route for logging in
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    message = ""
    # If the form is submitted and validated, log the user in
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            message += "You have been logged in!"
            flash(message, "success")
            return redirect(url_for("home"))
        else:
            message += "Login Unsuccessful. Please check email and password"
            flash(message, "danger")
    # If the form is submitted but not validated, show an error message
    elif form.is_submitted():
        message += "Form is invalid"
        flash(message, "danger")
    # Render the login template with the form
    return render_template("login.html", title="Login", page="login", form=form)


# Route for registering a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    message = ""
    # If the form is submitted and validated, create a new user
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        message += f"Account created for {form.username.data}!"
        flash(message, "success")
        return redirect(url_for("home"))
    # If the form is submitted but not validated, show an error message
    elif form.is_submitted():
        message += "Form is invalid"
        flash(message, "danger")
    # Render the register template with the form
    return render_template(
        "register.html",
        title="Register",
        page="register",
        form=form,
        message=message,
    )


# Route for logging out
@app.route("/logout", methods=["GET", "POST"])
def logout():
    form = LogoutForm()
    message = ""
    # If the form is submitted, log the user out
    if form.validate_on_submit():
        logout_user()
        message += "You have been logged out!"
        flash(message, "success")
        return redirect(url_for("home"))
    # If the form is submitted but not validated, show an error message
    elif form.is_submitted():
        message += "Form is invalid"
        flash(message, "danger")
    # Render the logout template with the form
    return render_template("logout.html", title="Logout", page="logout", form=form)


# Route for creating a new post
@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    message = ""
    # If the form is submitted and validated, create a new post
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data, content=form.content.data, user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        message += f"Post created for {form.title.data}!"
        flash(message, "success")
        return redirect(url_for("home"))
    # If the form is submitted but not validated, show an error message
    elif form.is_submitted():
        message += "Form is invalid"
        flash(message, "danger")
    # Render the create_post template with the form
    return render_template(
        "create_post.html",
        title="Create Post",
        page="create_post",
        form=form,
    )


# Route for viewing an individual post
@app.route("/post/<int:post_id>")
def post(post_id):
    # Query the post by ID or return 404 if not found
    post = Posts.query.get_or_404(post_id)
    # Render the post template with the post data
    return render_template("post.html", title=post.title, post=post, page="post")


# Route for viewing all posts
@app.route("/posts")
def posts():
    # Query all posts from the database
    all_posts = Posts.query.all()
    # Render the posts template with all posts
    return render_template("posts.html", title="All Posts", posts=all_posts)


# Route for updating a post
@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    # Query the post by ID or return 404 if not found
    post = Posts.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.author != current_user:
        flash("You are not authorized to update this post", "danger")
        return redirect(url_for("home"))
    form = CreatePostForm()
    # If the form is submitted and validated, update the post
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("post", post_id=post.id))
    # If the request method is GET, pre-fill the form with the current post data
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    # Render the create_post template with the form
    return render_template(
        "update_post.html", title="Update Post", form=form, post=post
    )


# route to delete a post
@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You are not authorized to delete this post", "danger")
        return redirect(url_for("home"))
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("home"))


# user profile route, show and update user profile
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template(
        "user_profile_page.html", title="Profile", form=form, page="profile"
    )


# Main entry point to run the app
if __name__ == "__main__":
    app.run(debug=True)
