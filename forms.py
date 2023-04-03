from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class SignUpForm(FlaskForm):
    full_name = StringField(
        "Full Name",
        validators=[
            InputRequired(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    password = PasswordField(
        "New Password",
        validators=[InputRequired()],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            InputRequired(),
            Email(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    password = PasswordField(
        "New Password",
        validators=[InputRequired()],
    )
    submit = SubmitField("Login")
