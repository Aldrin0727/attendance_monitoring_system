from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 

leave_bp = Blueprint('leave_bp', __name__)

@leave_bp.route('/leave_details', methods=['POST'])
def get_leave_details():
    try:   
        # get leave details
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

        username = data.get("username")
        position = data.get("position")
        department = data.get("department")
        address = data.get("address")
        contact = data.get("contact")
        leave_type = data.get("selectedTypeofLeave")
        total_leave = data.get("total_leave")
        leave_from = data.get("leaveForm.date_from")
        leave_to = data.get("leaveForm.date_to")
        leave_reason = data.get("leave_reason")

        # database insert
        # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute(
        #     "INSERT INTO Leave_Details (user,position,department,address,contact,leave_type,leave_number,leave_from,leave_to,leave_reason) VALUES (%s, %s)"
        # )
        
    except Exception as e:
        return jsonify({"error": str(e)}),500

