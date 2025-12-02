from flask import Blueprint, request, jsonify, session # type: ignore
import hashlib
from plugins import mysql 
import MySQLdb.cursors # type: ignore
from flask_mysqldb import MySQL # type: ignore
from config import Config

users_bp = Blueprint('users', __name__)

@users_bp.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data.get('username')
    password =data.get('password')

    if not username and not password:
        return jsonify({"error": "Username and Password is Missing."}),400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # cursor.execute("SELECT * FROM users WHERE username = %s AND acc_status = 1", (username,))
    query = f"""
        SELECT 
            u.*,
            u.department AS dept_code,
            d.department AS department_name   
        FROM `{Config.MYSQL_DB2}`.`users` AS u
        LEFT JOIN `{Config.MYSQL_DB2}`.`departments` AS d
            ON u.department = d.dept_code
        WHERE u.username = %s
        AND u.acc_status = 1
    """

    cursor.execute(query, (username,))
    # cursor.execute("SELECT * FROM `ticketing_dev`.`users` WHERE username = %s AND acc_status = 1", (username,))
    
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
        "department_name": user["department_name"],
        "dept_code": user["dept_code"],
        "first_login": user["first_login"],
        "role": user["role"],
        "job_title": user["job_title"],
    }

    return jsonify({
        "message": "Login successful",
        "user": session["user"]
    }), 200

<<<<<<< HEAD

=======
>>>>>>> 01f8ed9e1fb6c8e821703e0f76541f1bdf9743e3
@users_bp.route('/get_depthead', methods=['POST'])
def get_depthead():  
   try:
        data = request.get_json()
        department = data.get("department_name")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT id, first_name, last_name, email, department
<<<<<<< HEAD
            FROM users
=======
            FROM `{Config.MYSQL_DB2}`.users
>>>>>>> 01f8ed9e1fb6c8e821703e0f76541f1bdf9743e3
            WHERE job_title = 'Department Head' AND acc_status = 1 AND department = %s
        """, (department,))  

        heads = cursor.fetchall()
        cursor.close()

        return jsonify(heads), 200
   except Exception as e:
        return jsonify({"error": str(e)}), 

