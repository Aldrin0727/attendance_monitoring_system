from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime
from config import Config
ot_ob_bp = Blueprint('ot_ob_bp', __name__)

@ot_ob_bp.route('/create_ob_ot_request', methods=['POST'])
def create_request():
    try: 
        data = request.get_json()
        emp_id = data.get("emp_id")
        fullName = data.get("fullName")
        type = data.get("type")  # Avoid using 'type' as it is a Python keyword
        category = data.get("category")
        destination = data.get("destination")
        req_from = data.get("req_from")
        req_to = data.get("req_to")
        reason = data.get("reason")
        project = data.get("project")
        department = data.get("department")
                    
        year = datetime.now().year

        if type == "OB":
            ref_var = f"OB{year}"
        else:
            ref_var = f"OT{year}"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT ref_number FROM ot_ob 
            WHERE ref_number LIKE %s 
            ORDER BY otob_id DESC LIMIT 1
        """, (ref_var + '%',))

        result = cursor.fetchone()

        if result and result['ref_number']:
            last_ref = result['ref_number']
            ref_sequence = int(last_ref[-5:]) + 1
        else:
            ref_sequence = 1

        newref_No = f"{type}{year}{str(ref_sequence).zfill(5)}"

        cursor.execute(
            "INSERT INTO ot_ob (emp_id,fullName,type,category,destination,req_from,req_to,request_reason,project,date_created,status,ref_number,department) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)",
            (emp_id, fullName, type, category, destination, req_from, req_to,reason,project, 'FOR DEPARTMENT HEAD APPROVAL', newref_No,department)
        )

        cursor.execute(
            """INSERT INTO otob_history (module, ref_number, action, `user`, date) 
            VALUES (%s, %s, %s, %s, NOW())""",
            ('APPROVAL', newref_No, 'New Request Has been submitted', fullName)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True, "ref_number": newref_No}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@ot_ob_bp.route('/get_otob_for_approval', methods=['POST'])
def get_otob_approval_list():
    try: 
        data = request.get_json()
        status = data.get("status") 
        job_title = data.get("job_title")
        department = data.get("department")
        emp_id = data.get("emp_id")

        # base_query = """
        #     SELECT * from ot_ob WHERE status = %s

        # """
        # values = [status]
        # if job_title == 'Department Head': 
        #     if status == 'FOR DEPARTMENT HEAD APPROVAL':
        #         base_query += " status = %s AND department = %s" 
        #         values.append(status, department)
        #     else:
        #         base_query += " AND emp_id = %s"
        #         values.append(emp_id)
        # else:
        #     base_query += " AND emp_id = %s"
        #     values.append(emp_id)

        if job_title == 'Department Head' and status == 'FOR DEPARTMENT HEAD APPROVAL':
            base_query = f"""
                SELECT * from ot_ob LEFT JOIN `{Config.MYSQL_DB2}`.users ON ot_ob.emp_id = `{Config.MYSQL_DB2}`.users.emp_id  WHERE status = %s and ot_ob.department = %s"""
            values = [status, department]
        else:
            base_query = f"""
                SELECT * from ot_ob LEFT JOIN `{Config.MYSQL_DB2}`.users ON ot_ob.emp_id = `{Config.MYSQL_DB2}`.users.emp_id WHERE ot_ob.emp_id = %s"""
            values = [emp_id]
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(base_query, tuple(values))
        forapp_list =  cursor.fetchall()

        cursor.close()
        return jsonify({"forapp_list":forapp_list, "success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@ot_ob_bp.route("/otob_approval_count", methods=['POST'])
def get_otob_count_approval():
    try:
        data = request.get_json()
        username = data.get("fullName")
        position = data.get("job_title")
        department = data.get("department")
        emp_id = data.get("emp_id")


        if position == "Department Head":
            app_qry ="""
            SELECT count(*) as app_count 
            from ot_ob 
            where department = %s 
            and status = 'FOR DEPARTMENT HEAD APPROVAL'
            """
            params = (department,)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(app_qry,params)
        app_count = cursor.fetchone()["app_count"]

        cursor.execute("""
            SELECT count(*) as otob_user_count from ot_ob where emp_id = %s and status = 'FOR DEPARTMENT HEAD APPROVAL'
        """, (emp_id,))  
        user_count = cursor.fetchone()["otob_user_count"]

        return jsonify({
            "app_count": app_count, 
            "success": True,
            "user_count" : user_count
            }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@ot_ob_bp.route('/date_otob_calendar', methods=['POST'])
def get_otob_calendar_date():
    try:
        data = request.get_json()
        department = data.get("dept_code")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        date_qry = f"""
                       SELECT * from ot_ob where department = %s"""
        values = [department] 
        cursor.execute(date_qry, tuple(values))
        dateall = cursor.fetchall()
        cursor.close()

        return jsonify({"success": True,"dateall":dateall}), 201

    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@ot_ob_bp.route('/update_approved_deny_otob', methods=['POST'])
def update_approved_deny_otob():
    try:  
        data = request.get_json()
        args = data.get("args")
        ref_number = data.get("ref_number")
        username = data.get("user")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if args == "APPROVED" :
            cursor.execute(
                "UPDATE  ot_ob set status = %s,approved_by = %s, date_approved = NOW() WHERE ref_number = %s",(args, username, ref_number))
            
            cursor.execute(
                """INSERT INTO otob_history (module, ref_number, action, `user`, date) 
                VALUES (%s, %s, %s, %s, NOW())""",
                ('APPROVAL', ref_number, 'Approved Request', username)
            )
        else:
            cursor.execute(
                "UPDATE  ot_ob set status = %s WHERE ref_number = %s",(args, ref_number))
            
            cursor.execute(
                """INSERT INTO otob_history (module, ref_number, action, `user`, date) 
                VALUES (%s, %s, %s, %s, NOW())""",
                ('APPROVAL', ref_number, 'Denied Request', username)
            )
        
        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True,"args":args,"ref_no":ref_number}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500