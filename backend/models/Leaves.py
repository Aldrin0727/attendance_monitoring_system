from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 

leave_bp = Blueprint('leave_bp', __name__)

@leave_bp.route('/leave_details', methods=['POST'])
def get_leave_details():
    try:   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from Leave_Details")
        leave_details = cursor.fetchall()
        cursor.close()
        return jsonify(leave_details), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
 
@leave_bp.route('/create_leave', methods=['POST'])
def add_leave_details():
    try: 
        data = request.get_json()

        
        
    except Exception as e:
        return jsonify({"error": str(e)}),500

