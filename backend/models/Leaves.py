# routes/dashboard_faves.py
from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from flask_mysqldb import MySQL

mysql = MySQL()

create_leave_bp = Blueprint('create_leave', __name__)

@create_leave_bp.route('/leave_details', methods=['POST'])
def get_leave_details():
    try:
        data = request.get_json()




        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from Leave_Details")
        leave_details = cursor.fetchall()
        cursor.close()
        return jsonify(leave_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500

