from flask import Flask, render_template, url_for, flash, redirect
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, LogoutForm, CreatePostForm
from models import db, User, Posts
from flask_dotenv import DotEnv

app = Flask(__name__)

DotEnv().init_app(app)
# import Flask class from flask module
app.config["SECRET_KEY"] = "df9980f341166cf2f58a0167a55a8f6e"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
# app.config["MESSAGE_FLASHING_OPTIONS"] = {"duration": 5}

db.init_app(app)
with app.app_context():
    db.create_all()
# ?create a migration instance
migrate = Migrate(app, db)
# ?create a login manager instance
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/home")
@login_required
# define a function for the route, pass in the template file, posts dict,
# and title
def home():  # put application's code here
    user_posts = Posts.query.all()
    return render_template("home.html", posts=user_posts, title="Home", page="home")


@app.route("/about")
def about():
    return render_template("about.html", title="About", page="about")


# route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    message = ""
    # query the database for the user
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if the user exists and the password is correct
        if user and user.check_password(form.password.data):
            # use a login function to log the user in
            login_user(user)
            message += f"You have been logged in!"
            flash(message, "success")
            return redirect(url_for("home"))
        else:
            message += f"Login Unsuccessful. Please check email and password"
            flash(message, "danger")
    elif form.is_submitted():
        message += f"Form is invalid"
        flash(message, "danger")
    return render_template("login.html", title="Login", page="login", form=form)


# route for register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    message = ""
    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        message += f"Account created for {form.username.data}!" f" {user.username}"
        flash(message, "success")
        return redirect(url_for("home"))
    elif form.is_submitted():
        message += "Form is invalid"
        flash(message, "danger")
    return render_template(
        "register.html",
        title="Register",
        page="register",
        form=form,
        message=message,
    )


# route for logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    form = LogoutForm()
    message = ""
    if form.validate_on_submit():
        logout_user()
        message += f"You have been logged out!"
        flash(message, "success")
        return redirect(url_for("home"))
    elif form.is_submitted():
        message += f"Form is invalid"
        flash(message, "danger")
    return render_template("logout.html", title="Logout", page="logout", form=form)


# route for create_posts
@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    message = ""
    if form.validate_on_submit():
        post = Posts(
            title=form.title.data, content=form.content.data, user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        message += f"Post created for {form.title.data}!"
        flash(message, "success")
        return redirect(url_for("home"))
    elif form.is_submitted():
        message += f"Form is invalid"
        flash(message, "danger")
    return render_template(
        "create_post.html",
        title="Create Post",
        page="create_post",
        form=form,
    )


if __name__ == "__main__":
    app.run(debug=True)
