from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length


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


class SignUpForm(LoginForm):
    full_name = StringField(
        "Full Name",
        validators=[
            InputRequired(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Sign Up")


class EditPetForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            InputRequired(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    age = StringField(
        "Age",
        validators=[
            InputRequired(),
            Length(
                min=-1, max=100, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    bio = StringField(
        "Bio",
        validators=[
            InputRequired(),
            Length(
                min=-1, max=300, message="The maximum length of the string is %(max)d"
            ),
        ],
    )
    submit = SubmitField("Edit")
