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
        username = data.get("fullName")
        department = data.get("department_name")
        leave_type = data.get("selectedTypeofLeave")
        total_leave = data.get("total_leave_days") 
        leave_from = data.get("date_from")
        leave_to = data.get("date_to")
        leave_reason = data.get("leave_reason")
        status = 'FOR APPROVAL'
        approver = 'test'

        # database insert
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            INSERT INTO Leave_Details (
                user, leave_type, leave_number, leave_from, leave_to, leave_reason, date_created, department, status, approver
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s ,%s)
        """, (
            username, leave_type, total_leave, leave_from, leave_to, leave_reason, department, status, approver
        ))

        
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Submitted Leave is now For Approval.", "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500

