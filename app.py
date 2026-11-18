#from flask import Flask, render_template, request
#import re

#app = Flask(__name__)

#users = {}  # Stores accounts as {username: password}

#def valid_password(password):
 #   if len(password) < 8:
  #      return "Password must be at least 8 characters long."
   # if not re.search(r"\d", password):
    #    return "Password must contain at least one digit."
    #if not re.search(r"[a-z]", password):
     #   return "Password must contain at least one lowercase letter."
    #if not re.search(r"[A-Z]", password):
     #   return "Password must contain at least one uppercase letter."
    #if not re.search(r"[!@#$%^&*()_+=\-\[\]{};:,.<>/?]", password):
     #   return "Password must contain at least one symbol."

    #return None

#@app.route("/")
#def home():
 #   return render_template("home.html")


#@app.route("/signup", methods=["GET", "POST"])
#def signup():
 #   message = ""
  #  if request.method == "POST":
   #     username = request.form["username"]
    
    #    if username in users:
     #       message = "Username already exists."
      #  else:
       #     error = valid_password(password)
        ###  else:
           #     users[username] = password
            #    message = "Account created successfully!"

#    return render_template("signup.html", message=message)


#@app.route("/login", methods=["GET", "POST"])
#def login():
 #   message = ""
  #  if request.method == "POST":
   ##    password = request.form["password"]

     #   if username not in users:
      #      message = "No such user. Please sign up first."
       # elif users[username] == password:
        #    message = f"Login successful! Welcome, {username}"
        #else:
         #   message = "Incorrect password."

    #return render_template("login.html", message=message)


#if __name__ == "__main__":
 #   app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import re

# ---------------------------------
# Flask Setup
# ---------------------------------

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------------------------
# Database Model
# ---------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

# ---------------------------------
# Password Validation
# ---------------------------------

def valid_password(password):

    if len(password) < 8:
        return "Password must be at least 8 characters long."

    if not re.search(r"\d", password):
        return "Password must contain at least one digit."

    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."

    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."

    if not re.search(
        r"[!@#$%^&*()\-_=+\[\]{};:,.<>/?]",
        password
    ):
        return "Password must contain at least one symbol."

    return None

# ---------------------------------
# Home Page
# ---------------------------------

@app.route("/")
def home():
    return redirect(url_for("signup"))

# ---------------------------------
# Signup Page
# ---------------------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():

    error = ""
    success = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            error = "Username already exists."

        else:

            password_error = valid_password(password)

            if password_error:
                error = password_error

            else:

                hashed_password = generate_password_hash(
                    password
                )

                new_user = User(
                    username=username,
                    password=hashed_password
                )

                db.session.add(new_user)
                db.session.commit()

                success = "Account created successfully!"

    return render_template(
        "signup.html",
        error=error,
        success=success
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    return render_template(
        "login.html",
        error=error
    )

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        username=current_user.username
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ---------------------------------
# Create Database
# ---------------------------------

with app.app_context():
    db.create_all()

# ---------------------------------
# Run Application
# ---------------------------------

if __name__ == "__main__":
    app.run(debug=True)

