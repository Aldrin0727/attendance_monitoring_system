from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime
from config import Config
leave_bp = Blueprint('leave_bp', __name__)


 
 
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
        emp_id = data.get("emp_id")
        # approver = 'test'
       
        year = datetime.now().year

        # database insert
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT MAX(ref_no) as ref from Leave_Details
        """) 
        result = cursor.fetchone()

        if result and result['ref']:
            last_ref = result['ref']
            ref_sequence = int(last_ref[-4:]) + 1
        else:
            ref_sequence = 1

        newref_No = f"{year}{str(ref_sequence).zfill(4)}"

        cursor.execute(
            "INSERT INTO Leave_Details (`user`,ref_no,leave_type,leave_number,leave_from,leave_to,leave_reason,date_created,department,status,emp_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)",
            (username, newref_No, leave_type, total_leave, leave_from, leave_to, leave_reason,
            department, 'FOR DEPARTMENT HEAD APPROVAL', emp_id)
        )

<<<<<<< HEAD
        cursor.execute(
            """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
            VALUES (%s, %s, %s, %s, NOW())""",
            ('CREATE', newref_No, 'New Leave Request Has been submitted', username)
=======
        # cursor.execute(
        #     """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
        #     VALUES (%s, %s, %s, %s, NOW())""",
        #     ('CREATE', newref_No, 'New Leave Request Has been submitted', username)
        # )

        cursor.execute(
            """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
            VALUES (%s, %s, %s, %s, NOW())""",
            ('APPROVAL', newref_No, 'New Leave Request Has been submitted', username)
>>>>>>> origin/lj_branch
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "message": "Submitted Leave is now For Approval.",
            "success": True,
            "ref_no": newref_No
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
<<<<<<< HEAD
    
=======
>>>>>>> origin/lj_branch
    
@leave_bp.route("/for_approval_count", methods=['POST'])
def get_count_approval():
    try:
        data = request.get_json()
        username = data.get("fullName")
        position = data.get("job_title")
        department = data.get("department")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

       
       

        if position == "Department Head":
            app_qry ="""
            SELECT count(*) as app_count 
            from Leave_Details 
            where department = %s 
            and status = 'FOR DEPARTMENT HEAD APPROVAL'
            """
            params = (department,)
            
        else:
            app_qry ="""
            SELECT count(*) as app_count 
            from Leave_Details 
            where user = %s 
            and status = 'FOR DEPARTMENT HEAD APPROVAL'
              """
            params = (username,)
            
        cursor.execute(app_qry,params)
        app_count = cursor.fetchone()["app_count"]
      
        cursor.execute("""
            SELECT count(*) as fapp_count from Leave_Details where user = %s and status = 'FOR DEPARTMENT HEAD APPROVAL'
        """, (username,))  
        fapp_count = cursor.fetchone()["fapp_count"]

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
            "app_count": app_count, "success": True,"fapp_count":fapp_count,"fullName": username, "used_vl":used_vl,"used_sl":used_sl
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@leave_bp.route('/leave_list', methods=['POST'])
def get_leave_list():
    try:   
        data = request.get_json()
        username = data.get("fullName")
        status = data.get("status")
        department = data.get("department_name")
        position = data.get("job_title")
        

        base_query = """
            SELECT * from Leave_Details WHERE status = %s

        """
        values = [status]
        if position == 'Department Head': 
            if status == 'FOR DEPARTMENT HEAD APPROVAL':
                base_query += " AND department = %s" 
                values.append(department)
            else:
                base_query += " AND user = %s"
                values.append(username)
        else:
            base_query += " AND user = %s"
            values.append(username)
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(base_query, tuple(values))
        forapp_list =  cursor.fetchall()

        cursor.close()
        return jsonify({"forapp_list":forapp_list, "success": True}), 201
    
    #    return jsonify({"forapp_list":forapp_list,"app_list":app_list,"success":True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
 
@leave_bp.route('/all_leave_details', methods=['POST'])
def get_all_leave_details():
    try:   
        # get leave details
        data = request.get_json()
        username = data.get("fullName")
        status = data.get("status")
        leave_type = data.get("leave_type")
        position = data.get("job_title")
        department = data.get("dept_code")

        
        if position == 'Department Head' and status == 'FOR DEPARTMENT HEAD APPROVAL':
            base_query = f"""
                    SELECT * ,
                    (SELECT `{Config.MYSQL_DB2}`.departments.department from Leave_Details LEFT JOIN `{Config.MYSQL_DB2}`.departments ON Leave_Details.department = dept_code
                    where Leave_Details.department = "ITD" group by department) as dept_code
                    FROM Leave_Details 
                    LEFT JOIN `{Config.MYSQL_DB2}`.users
                        ON Leave_Details.emp_id = ticketing_dev.users.emp_id
                    WHERE Leave_Details.department = %s
                    """
            values = [department]
        else:          
            # base_query = """
            #     SELECT * from Leave_Details WHERE user = %s
            # """
            base_query = f"""
                    SELECT * ,
                    (SELECT `{Config.MYSQL_DB2}`.departments.department from Leave_Details LEFT JOIN `{Config.MYSQL_DB2}`.departments ON Leave_Details.department = dept_code
                    where Leave_Details.department = "ITD" group by department) as dept_code
                    FROM Leave_Details 
                    LEFT JOIN `{Config.MYSQL_DB2}`.users
                        ON user = CONCAT(first_name, ' ', last_name)
                    WHERE Leave_Details.user = %s
                    """
            values = [username]

        if status:
            base_query += " AND status = %s"
            values.append(status)

        if leave_type:
            base_query += " AND leave_type = %s"
            values.append(leave_type)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(base_query, tuple(values))
        all_list =  cursor.fetchall()

        cursor.close()
        return jsonify({"all_list":all_list, "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@leave_bp.route('/approved_deny_leaves', methods=['POST'])
def update_approved__deny_leaves():
    try:  
        data = request.get_json()
        args = data.get("args")
        ref_no = data.get("ref_no")
<<<<<<< HEAD
        username = data.get("fullName")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "UPDATE  Leave_Details set status = %s WHERE ref_no = %s",(args, ref_no))
=======
        username = data.get("user")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "UPDATE  Leave_Details set status = %s,approved_by = %s, date_approved = NOW() WHERE ref_no = %s",(args, username, ref_no))
>>>>>>> origin/lj_branch
        
        cursor.execute(
            """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
            VALUES (%s, %s, %s, %s, NOW())""",
            ('APPROVAL', ref_no, 'Approved Leave', username)
        )
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True,"args":args,"ref_no":ref_no}), 201
    except Exception as e:
<<<<<<< HEAD
        return jsonify({"error": str(e)}),500
=======
        return jsonify({"error": str(e)}),500
    
@leave_bp.route('/date_calendar', methods=['POST'])
def get_calendar_date():
    try:
        data = request.get_json()
        department = data.get("dept_code")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        date_qry = f"""
                       SELECT * from Leave_Details where department = %s"""
        values = [department] 
        cursor.execute(date_qry, tuple(values))
        dateall = cursor.fetchall()
        cursor.close()

        return jsonify({"success": True,"dateall":dateall}), 201

    except Exception as e:
        return jsonify({"error": str(e)}),500
>>>>>>> origin/lj_branch
