from flask import Blueprint, request, jsonify, session # type: ignore
import hashlib
from plugins import mysql 
import MySQLdb.cursors # type: ignore
from flask_mysqldb import MySQL # type: ignore

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data.get('username')
    password =data.get('password')

    if not username and not password:
        return jsonify({"error": "Username and Password is Missing."}),400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s AND acc_status = 1", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user :
        return jsonify({"error": "Invalid Username."}), 401

    if hashlib.sha256(password.encode()).hexdigest() != user["password"]:
        return jsonify({"error": "Invalid username or password."}), 401
    
    if user["first_login"]:
        return jsonify({
            "message": "First login, please change your password.",
            "first_login": 0,
            "first_name": user["first_name"]
        }), 200

        session["user"] = {
        "id": user["id"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "username": user["username"],
        "email": user["email"],
        "department": user["department"],
        "first_login": user["first_login"],
        "role": user["role"],
        "job_title": user["job_title"],
    }

    return jsonify({
        "message": "Login successful",
        "user": session["user"]
    }), 200