from flask import Flask, request, render_template, abort, session, redirect, url_for
from forms import LoginForm, SignUpForm
from flask_session import Session

import os

SECRET_KEY = os.getenv("SECRET_KEY")


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = [
    {
        "id": 1,
        "full_name": "Pet Rescue Team",
        "email": "team@pawsrescue.co",
        "password": "adminpass",
    },
]

pets = [
    {
        "id": 1,
        "name": "Nelly",
        "age": "5 weeks",
        "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.",
    },
    {
        "id": 2,
        "name": "Yuki",
        "age": "8 months",
        "bio": "I am a handsome gentle-cat. I like to dress up in bow ties.",
    },
    {
        "id": 3,
        "name": "Basker",
        "age": "1 year",
        "bio": "I love barking. But, I love my friends more.",
    },
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]


@app.route("/")
def home():
    return render_template("home.html", pets=pets)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        users.append(
            {
                "id": len(users) + 1,
                "ful_name": form.full_name.data,
                "email": form.email.data,
                "password": form.password.data,
            }
        )
        return redirect(url_for("login", _scheme="http", _external=True))
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for user in users:
            if (
                user["email"] == form.email.data
                and user["password"] == form.password.data
            ):
                session["email"] = form.email.data
                return render_template(
                    "login.html",
                    form=form,
                    message="Successfully Logged In",
                )
        return render_template(
            "login.html",
            form=form,
            message="Incorrect Email or Password",
        )
    elif form.errors:
        print(form.errors.items())
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    if "email" in session:
        session.pop("email", None)
    return redirect(url_for("login", _scheme="http", _external=True))


@app.route("/details/<int:pet_id>")
def pet_details(pet_id):
    pet = next(filter(lambda pet: pet["id"] == pet_id, pets), None)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    else:
        return render_template("detail.html", pet=pet)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
