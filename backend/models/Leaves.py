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
        approver = 'test'

        # database insert
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO Leave_Details (user,leave_type,leave_number,leave_from,leave_to,leave_reason,date_created,department,status,approver) " \
            "VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s ,%s)",(username,leave_type,total_leave,leave_from,leave_to,leave_reason,department,'FOR DEPARTMENT HEAD APPROVAL',approver) )
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Submitted Leave is now For Approval.","success":True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@leave_bp.route("/for_approval_count", methods=['POST'])
def get_count_approval():
    try:
        data = request.get_json()
        username = data.get("fullName")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT count(*) as app_count from Leave_Details where user = %s and status = 'FOR DEPARTMENT HEAD APPROVAL'
        """, (username,))  
        app_count = cursor.fetchone()["app_count"]

        cursor.execute("""
            SELECT count(*) as used_vl from Leave_Details where user = %s and status = 'APPROVED' and (leave_type = 'VL' || leave_type = 'EL')
        """, (username,))  
        used_vl = cursor.fetchone()["used_vl"]

        cursor.execute("""
            SELECT count(*) as used_sl from Leave_Details where user = %s and status = 'APPROVED' AND leave_type = 'SL'
        """, (username,))  
        used_sl = cursor.fetchone()["used_sl"]
        
        cursor.close()

        return jsonify({
            "app_count": app_count, 
            "success": True, 
            "used_sl" : used_sl, 
            "used_vl":used_vl
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500
    

@leave_bp.route('/leave_list', methods=['POST'])
def get_leave_list():
    try:   
        data = request.get_json()
        username = data.get("fullName")
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT 
               *
            FROM Leave_Details 
            WHERE user = %s 
              AND status = 'FOR DEPARTMENT HEAD APPROVAL'
        """, (username,))
        # forapp_list = [row[0] for row in cursor.fetchall()]
        forapp_list = cursor.fetchall()
       

        # cursor.execute("SELECT * from Leave_Details where user = %s and status = 'APPROVED' ",(username))
        # app_list = [row[0] for row in cursor.fetchall()]

        cursor.close()
        return jsonify({"data":forapp_list, "success": True}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}),500
    


