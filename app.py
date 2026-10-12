from flask import Flask, render_template, request
import re

app = Flask(__name__)

users = {}  # Stores accounts as {username: password}

def valid_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[!@#$%^&*()_+=\-\[\]{};:,.<>/?]", password):
        return "Password must contain at least one symbol."

    return None

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            message = "Username already exists."
        else:
            error = valid_password(password)
            if error:
                message = error
            else:
                users[username] = password
                message = "Account created successfully!"

    return render_template("signup.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in users:
            message = "No such user. Please sign up first."
        elif users[username] == password:
            message = f"Login successful! Welcome, {username}"
        else:
            message = "Incorrect password."

    return render_template("login.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)