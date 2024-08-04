from flask import Flask, render_template, url_for, flash, redirect
from flask_login import LoginManager, login_user
from flask_migrate import Migrate
from posts import posts
from forms import RegistrationForm, LoginForm, LogoutForm
from models import db, User
from flask_dotenv import DotEnv

app = Flask(__name__)

DotEnv().init_app(app)
# import Flask class from flask module
app.config["SECRET_KEY"] = "df9980f341166cf2f58a0167a55a8f6e"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)
with app.app_context():
    db.create_all()
# ?create a migration instance
migrate = Migrate(app, db)
# ?create a login manager instance
login_manager = LoginManager(app)
login_manager.init_app(app)


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/home")
# define a function for the route, pass in the template file, posts dict,
# and title
def home():  # put application's code here
    return render_template("home.html", posts=posts, title="Home", page="home")


@app.route("/about")
def about():
    return render_template("about.html", title="About", page="about")


# route for login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # query the database for the user
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # check if the user exists and the password is correct
        if user and user.password == form.password.data:
            # use login function to log the user in
            login_user(user)
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
    else:
        flash("Form is invalid", "danger")
        return render_template("login.html", title="Login", page="login", form=form)


# route for register
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            is_active=True,
        )
        db.session.add(user)
        db.session.commit()

        message = f"Account created for {form.username.data}! {user.username}"
        flash(message, "success")
        return redirect(url_for("home"))
    else:
        flash("Form is invalid", "danger")
        return render_template(
            "register.html", title="Register", page="register", form=form
        )


# route for logout
@app.route("/logout", methods=["GET", "POST"])
def logout():
    form = LogoutForm()
    message = ""
    if form.validate_on_submit():
        message = "You have been logged out!"
        flash(message, "success")
        return redirect(url_for("home"))
    else:
        flash("Form is invalid", "danger")
        return render_template("logout.html", title="Logout", page="logout", form=form)


if __name__ == "__main__":
    app.run(debug=True)
