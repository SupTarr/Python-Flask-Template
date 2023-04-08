from flask import Flask, render_template, abort, session, redirect, url_for
from forms import LoginForm, SignUpForm, EditPetForm
from flask_session import Session
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy

import os

SECRET_KEY = os.getenv("SECRET_KEY")


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://%s:%s@%s:%s/%s" % (
    os.getenv("DATABASE_USERNAME"),
    quote_plus(os.getenv("DATABASE_PASSWORD")),
    os.getenv("DATABASE_HOSTNAME"),
    os.getenv("DATABASE_PORT"),
    os.getenv("DATABASE_NAME"),
)
Session(app)
db = SQLAlchemy(app)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    age = db.Column(db.String, nullable=False)
    bio = db.Column(db.String, nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    pets = db.relationship("Pet", backref="user")


def create_data():
    with app.app_context():
        db.create_all()

        team = User(
            full_name="Pet Rescue Team", email="team@petrescue.co", password="adminpass"
        )
        db.session.add(team)

        nelly = Pet(
            name="Nelly",
            age="5 weeks",
            bio="I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.",
        )
        yuki = Pet(
            name="Yuki",
            age="8 months",
            bio="I am a handsome gentle-cat. I like to dress up in bow ties.",
        )
        basker = Pet(
            name="Basker",
            age="1 year",
            bio="I love barking. But, I love my friends more.",
        )
        mrfurrkins = Pet(name="Mr. Furrkins", age="5 years", bio="Probably napping.")

        db.session.add(nelly)
        db.session.add(yuki)
        db.session.add(basker)
        db.session.add(mrfurrkins)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()


create_data()


@app.route("/")
def home():
    return render_template("home.html", pets=Pet.query.all())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        db.session.add(
            User(
                full_name=form.full_name.data,
                email=form.email.data,
                password=form.password.data,
            )
        )
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template(
                "signup.html",
                form=form,
                message="This Email already exists in the system! Please Log in instead.",
            )
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully signed up")
    elif form.errors:
        print(form.errors.items())
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (
            User.query.filter_by(
                email=form.email.data, password=form.password.data
            ).first()
            != None
        ):
            session["email"] = form.email.data
            return render_template(
                "login.html",
                form=form,
                message="Successfully Logged In",
            )
        else:
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


@app.route("/details/<int:pet_id>", methods=["POST", "GET"])
def pet_details(pet_id):
    form = EditPetForm()
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    elif form.validate_on_submit():
        pet.name = form.name.data
        pet.age = form.age.data
        pet.bio = form.bio.data
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template(
                "details.html",
                pet=pet,
                form=form,
                message="A Pet with this name already exists!",
            )
        finally:
            db.session.close()
        return redirect(url_for("home", _scheme="http", _external=True))
    else:
        return render_template("detail.html", pet=pet, form=form)


@app.route("/delete/<int:pet_id>")
def delete_pet(pet_id):
    pet = Pet.query.get(pet_id)
    if pet is None:
        abort(404, description="No Pet was Found with the given ID")
    db.session.delete(pet)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(url_for("home", _scheme="http", _external=True))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
