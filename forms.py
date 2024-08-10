from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    SubmitField,
    BooleanField,
)
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        [DataRequired()],
    )
    email = EmailField("Email Address", [DataRequired(), Email()])
    password = PasswordField("New Password", [DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Repeat Password", [EqualTo("password")])
    submit = SubmitField("Register")


# TODO: Add validators to the form fields in the form class above.
class LoginForm(FlaskForm):

    # username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [DataRequired()])
    email = EmailField("Email Address", [DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class LogoutForm(FlaskForm):
    submit = SubmitField("Logout")


class CreatePostForm(FlaskForm):
    title = StringField("Title", [DataRequired()])
    content = StringField("Content", [DataRequired()])
    submit = SubmitField("Post")
