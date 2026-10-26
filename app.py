
from flask import Flask, render_template, jsonify, request
from database import get_db_connection

app = Flask(__name__)

#basic homepage urlpath. For now just displays whatever is in temapltes > index.html (nothing currently)
@app.route("/")
def home():
    return render_template("index.html")

#display the login page
@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

#get route
@app.route("/api/users", methods=["GET"])
def get_users():
    connection = get_db_connection()

    user_count = connection.execute(
        "SELECT COUNT(*) FROM users"
    ).fetchone()[0]

    connection.close()

    return f"Internship Tracker backend is running! Users in database: {user_count}"

#below code will be used to get internships from the database and return them as JSON at the /api/internships url path.
@app.route("/api/internships", methods=["GET"])
def get_internships():
    connection = get_db_connection()

    internships = connection.execute(
        "SELECT * FROM internships"
    ).fetchall()

    connection.close()

    return jsonify([dict(internship) for internship in internships])

#below code will be used to add internships to the database via a POST request to the /api/internships url path.
@app.route("/api/internships", methods=["POST"])
def add_internship():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON data"}), 400

    company = data.get("company")
    position = data.get("position")
    status = data.get("status", "Interested")

    if not isinstance(company, str) or not company.strip():
        return jsonify({"error": "Company is required"}), 400

    if not isinstance(position, str) or not position.strip():
        return jsonify({"error": "Position is required"}), 400

    valid_statuses = ["Interested", "Applied", "Interview", "Offer", "Rejected"]

    if status not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    connection = get_db_connection()

    #temporary test user until we implement login stuff
    user_id = 1

    user = connection.execute(
        "SELECT id FROM users WHERE id = ?", (user_id,)
    ).fetchone()

    if user is None:
        connection.close()
        return jsonify({"error": "Test user does not exist yet"}), 400

    cursor = connection.execute(
        """
        INSERT INTO internships (user_id, company, position, status)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, company.strip(), position.strip(), status)
    )

    connection.commit()
    internship_id = cursor.lastrowid
    connection.close()

    return jsonify({
        "message": "Internship added successfully",
        "id": internship_id
    }), 201


#start flask 
if __name__ == "__main__":
    app.run(debug=True)
