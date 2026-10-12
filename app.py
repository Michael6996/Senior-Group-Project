
from flask import Flask
from database import get_db_connection

app = Flask(__name__)


@app.route("/")
def home():
    connection = get_db_connection()

    user_count = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    connection.close()

    return f"Internship Tracker backend is running! Users in database: {user_count}"


if __name__ == "__main__":
    app.run(debug=True)
