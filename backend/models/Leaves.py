from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime
from config import Config

from plugins import mail
from emails import send_vl_leave_request_email, send_leave_for_approval_email

leave_bp = Blueprint('leave_bp', __name__)

def expire_pending_vl():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT ref_no, user
        FROM Leave_Details
        WHERE leave_type = 'VL'
          AND status = 'FOR DEPARTMENT HEAD APPROVAL'
          AND DATE(leave_from) < CURDATE()
    """)
    rows = cursor.fetchall()

    if rows:
        cursor.execute("""
            UPDATE Leave_Details
            SET status = 'CANCELLED'
            WHERE leave_type = 'VL'
              AND status = 'FOR DEPARTMENT HEAD APPROVAL'
              AND DATE(leave_from) < CURDATE()
        """)

        cursor.executemany("""
            INSERT INTO leave_history (module, ref_no, action, `user`, history_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, [
            ('LEAVES', r['ref_no'], 'Auto-expired (Date From already passed)', r['user'])
            for r in rows
        ])

        mysql.connection.commit()

    cursor.close()

 
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
        halfday = data.get("halfday")
        max_leave = 15
        # approver = 'test'
       
        year = datetime.now().year
        if leave_type == 'SL':
            ref_var = 'SL'
        else:
            ref_var = 'VL'

        # database insert
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT ref_no from Leave_Details
            WHERE ref_no like %s
            ORDER BY id DESC LIMIT 1
        """,(ref_var + '%',)) 
        result = cursor.fetchone()

        if result and result['ref_no']:
            last_ref = result['ref_no']
            ref_sequence = int(last_ref[-5:]) + 1
        else:
            ref_sequence = 1

        newref_No = f"{ref_var}{year}{str(ref_sequence).zfill(5)}"

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as vl_leave from Leave_Details where emp_id = %s and status = 'APPROVED' and leave_type IN ("VL","EL")
        """, (emp_id,))  
        vl_leave = cursor.fetchone()["vl_leave"]

        vl_remaining = max_leave - vl_leave

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as sl_leave from Leave_Details where emp_id = %s and status = 'APPROVED' and leave_type IN ("SL")
        """, (emp_id,))  
        sl_leave = cursor.fetchone()["sl_leave"]

        sl_remaining = max_leave - sl_leave
        
        cursor.execute(
            "INSERT INTO Leave_Details (`user`,ref_no,leave_type,leave_number,leave_from,leave_to,leave_reason,date_created,department,status,emp_id,isHalfday,vl_remaining,sl_remaining) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s)",
            (username, newref_No, leave_type, total_leave, leave_from, leave_to, leave_reason,
            department, 'FOR DEPARTMENT HEAD APPROVAL', emp_id, halfday,vl_remaining,sl_remaining)
        )

        # cursor.execute(
        #     """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
        #     VALUES (%s, %s, %s, %s, NOW())""",
        #     ('CREATE', newref_No, 'New Leave Request Has been submitted', username)
        # )

        email_query = f"""
            SELECT email
            FROM `{Config.MYSQL_DB2}`.`users`
            WHERE job_title = 'Department Head'
            AND department = %s
            AND email IS NOT NULL
            AND email <> ''
        """

        cursor.execute(email_query, (department,))
        rows = cursor.fetchall()

        depthead_emails = [r["email"] for r in rows if r.get("email")]

        if depthead_emails:
            send_leave_for_approval_email(
                mail=mail,
                dept_head_emails=depthead_emails, 
                employee_name=username,
                ref_no=newref_No,
                dept=department,
                leave_type=leave_type,
                leave_number=total_leave,
                leave_from=leave_from,
                leave_to=leave_to,
                reason=leave_reason
            )


        cursor.execute(
            """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
            VALUES (%s, %s, %s, %s, NOW())""",
            ('LEAVE SUBMITTED', newref_No, 'New Leave Request Has been submitted', username)
        )

        


        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "message": "Submitted Leave is now For Approval.",
            "success": True,
            "ref_no": vl_remaining,
            "vl" : vl_remaining,
            "sl" : sl_remaining
        }), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500
    
@leave_bp.route("/for_approval_count", methods=['POST'])
def get_count_approval():
    try:
        expire_pending_vl()

        data = request.get_json()
        username = data.get("fullName")
        position = data.get("job_title")
        department = data.get("department")
        emp_id = data.get("emp_id")
        max_leave = 15
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
            where emp_id = %s 
            and status = 'FOR DEPARTMENT HEAD APPROVAL'
              """
            params = (emp_id,)
            
        cursor.execute(app_qry,params)
        app_count = cursor.fetchone()["app_count"]
      
        cursor.execute("""
            SELECT count(*) as fapp_count from Leave_Details where emp_id = %s and status = 'FOR DEPARTMENT HEAD APPROVAL'
        """, (emp_id,))  
        fapp_count = cursor.fetchone()["fapp_count"]

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_vl from Leave_Details where emp_id = %s and status = 'APPROVED' and (leave_type = 'VL' || leave_type = 'EL')
        """, (emp_id,))  
        used_vl = cursor.fetchone()["used_vl"]
 

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_sl from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type = 'SL'
        """, (emp_id,))  
        used_sl = cursor.fetchone()["used_sl"]

        # cursor.execute("""
        #     SELECT leave_number as vl_remaining from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ("VL","EL") ORDER BY id DESC
        # """, (emp_id,))  
        # vl_result = cursor.fetchone()
        # Vl_remaining = vl_result["vl_remaining"] if vl_result else 0

        # cursor.execute("""
        #     SELECT leave_number as sl_remaining from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ("SL") ORDER BY id DESC
        # """, (emp_id,))  
        # sl_result = cursor.fetchone()
        # sl_remaining = sl_result["sl_remaining"] if sl_result else 0

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_vl from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ('VL','EL')
        """, (emp_id,))  
        used_vl = cursor.fetchone()["used_vl"]

        remaining_vl = max_leave - used_vl 

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_sl from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ('SL')
        """, (emp_id,))  
        used_sl = cursor.fetchone()["used_sl"]

        remaining_sl = max_leave - used_sl 

        cursor.close()

        return jsonify({
            "app_count": app_count, "success": True,"fapp_count":fapp_count,"fullName": username, 
            "used_vl":used_vl,"used_sl":used_sl,"vl_remaining" : remaining_vl,"sl_remaining" :remaining_sl
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
@leave_bp.route('/leave_list', methods=['POST'])
def get_leave_list():
    try:
        expire_pending_vl()

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
        return jsonify({"forapp_list":forapp_list, "success": True}), 200
    
    #    return jsonify({"forapp_list":forapp_list,"app_list":app_list,"success":True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
 
@leave_bp.route('/all_leave_details', methods=['POST'])
def get_all_leave_details():
    try:
        expire_pending_vl()
        # get leave details
        data = request.get_json()
        username = data.get("fullName")
        status = data.get("status")
        leave_type = data.get("leave_type")
        position = data.get("job_title")
        department = data.get("dept_code")

        
        if position == 'Department Head' and status == 'FOR DEPARTMENT HEAD APPROVAL':
            base_query = f"""
                SELECT 
                    Leave_Details.*,
                    CAST(DATE(Leave_Details.leave_from) AS CHAR) AS leave_from,
                    CAST(DATE(Leave_Details.leave_to) AS CHAR) AS leave_to,
                    (SELECT d.department
                    FROM `{Config.MYSQL_DB2}`.departments d
                    WHERE d.dept_code = Leave_Details.department
                    LIMIT 1) AS dept_code
                FROM Leave_Details
                WHERE Leave_Details.department = %s
            """
            values = [department]

        else:          
            # base_query = """
            #     SELECT * from Leave_Details WHERE user = %s
            # """
            emp_id = data.get("emp_id")

            base_query = f"""
                SELECT 
                    Leave_Details.*,
                    CAST(DATE(Leave_Details.leave_from) AS CHAR) AS leave_from,
                    CAST(DATE(Leave_Details.leave_to) AS CHAR) AS leave_to,
                    (SELECT d.department
                    FROM `{Config.MYSQL_DB2}`.departments d
                    WHERE d.dept_code = Leave_Details.department
                    LIMIT 1) AS dept_code
                FROM Leave_Details
                WHERE Leave_Details.emp_id = %s
            """
            values = [emp_id]


        if status:
            base_query += " AND status = %s"
            values.append(status)

        if leave_type:
            base_query += " AND leave_type = %s"
            values.append(leave_type)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(base_query, tuple(values))

       


        all_list =  cursor.fetchall()
        for row in all_list:
            if row.get("leave_from"):
                row["leave_from"] = row["leave_from"].strftime("%Y-%m-%d")
            if row.get("leave_to"):
                row["leave_to"] = row["leave_to"].strftime("%Y-%m-%d")

        cursor.close()
        return jsonify({"all_list":all_list, "success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500
    
# @leave_bp.route('/approved_deny_leaves', methods=['POST'])
# def update_approved__deny_leaves():
#     try:  
#         args = request.form.get("args")
#         ref_no = request.form.get("ref_no")
#         username = request.form.get("user")
#         emp_id = request.form.get("emp_id")
#         pdf_file = request.files.get("pdf")

#         max_leave = 15
        

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

#         detail_qry =  f"""
#                 SELECT  
#                 *,
#                 (SELECT `{Config.MYSQL_DB2}`.departments.department from Leave_Details LEFT JOIN `{Config.MYSQL_DB2}`.departments ON Leave_Details.department = dept_code
#                     where Leave_Details.department = "ITD" group by department) as dept_code
#                 from Leave_Details LEFT JOIN `{Config.MYSQL_DB2}`.users ON Leave_Details.emp_id = ticketing_dev.users.emp_id where 
#                 ref_no = %s 
#                 """
#         values = [ref_no]
#         cursor.execute(detail_qry, tuple(values))
#         all_list =  cursor.fetchone()
#         #get number of leave
#         cursor.execute("""
#             SELECT leave_number as used_count from Leave_Details where ref_no = %s 
#         """, (ref_no,))  
#         row = cursor.fetchone() or {}
#         used_count = row.get("used_count", 0)

#         cursor.execute("""
#             SELECT COALESCE(SUM(leave_number), 0) as used_vl from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ('VL','EL')
#         """, (emp_id,))  
#         used_vl = cursor.fetchone()["used_vl"]

#         remaining_vl = max_leave - (used_vl + used_count)

#         cursor.execute("""
#             SELECT COALESCE(SUM(leave_number), 0) as used_sl from Leave_Details where emp_id = %s and status = 'APPROVED' AND leave_type IN ('SL')
#         """, (emp_id,))  
#         used_sl = cursor.fetchone()["used_sl"]

#         remaining_sl = max_leave - (used_sl + used_count)


#         cursor.execute("""
#             SELECT leave_type as leave_type from Leave_Details where ref_no = %s
#         """, (ref_no,))  
#         leave_type = cursor.fetchone()["leave_type"]

#         if args == "APPROVED" :
            
#             if leave_type == 'SL':
#                 cursor.execute(
#                 "UPDATE  Leave_Details set status = %s,approved_by = %s, sl_remaining = %s, date_approved = NOW() WHERE ref_no = %s",(args, username, remaining_sl, ref_no))
#             else:
#                 cursor.execute(
#                 "UPDATE  Leave_Details set status = %s,approved_by = %s, vl_remaining = %s, date_approved = NOW() WHERE ref_no = %s",(args, username, remaining_vl, ref_no))
            
#             cursor.execute(
#                 """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
#                 VALUES (%s, %s, %s, %s, NOW())""",
#                 ('LEAVE APPROVAL', ref_no, 'Approved Leave', username)
#             )

#             mysql.connection.commit() 

#             # RE-FETCH updated ro
#             cursor.execute(detail_qry, (ref_no,))
#             all_list = cursor.fetchone()

#             # Send email AFTER commit + refetch
#             if pdf_file:
#                 cursor.execute(detail_qry, (ref_no,))
#                 all_list = cursor.fetchone()

#                 send_vl_leave_request_email(
#                     mail,
#                     all_list['user'],
#                     ref_no,
#                     all_list['position'],
#                     all_list['dept_code'],
#                     all_list['leave_number'],
#                     all_list['leave_from'],
#                     all_list['leave_to'],
#                     all_list['leave_reason'],
#                     all_list['email'],
#                     all_list['leave_type'],
#                     pdf_file=pdf_file
#                 )
 
#         elif args == "CANCELLED" :
#             cursor.execute(
#                 "UPDATE  Leave_Details set status = %s WHERE ref_no = %s",(args, ref_no))
            
#             cursor.execute(
#                 """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
#                 VALUES (%s, %s, %s, %s, NOW())""",
#                 ('CANCEL LEAVE', ref_no, 'Cancelled Leave', username)
#             )
#         else:
#             cursor.execute(
#                 "UPDATE  Leave_Details set status = %s WHERE ref_no = %s",(args, ref_no))
            
#             cursor.execute(
#                 """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
#                 VALUES (%s, %s, %s, %s, NOW())""",
#                 ('LEAVE APPROVAL', ref_no, 'Denied Leave', username)
#             )
        
#         mysql.connection.commit()
#         cursor.close()

#         return jsonify({"success": True,"args":args,"leave_type":leave_type,"remaining_vl":remaining_vl}), 201
#     # "ref_no":all_list,
#     except Exception as e:
#         return jsonify({"error": str(e)}),500

@leave_bp.route('/approved_deny_leaves', methods=['POST'])
def update_approved__deny_leaves():
    try:
        args = request.form.get("args")
        ref_no = request.form.get("ref_no")
        username = request.form.get("user")
        emp_id = request.form.get("emp_id")
        pdf_file = request.files.get("pdf")
        department = request.form.get("dept_code")

        max_leave = 15
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ get current status + leave_type + leave_number
        cursor.execute("""
            SELECT status, leave_type, leave_number, department
            FROM Leave_Details
            WHERE ref_no = %s
            LIMIT 1
        """, (ref_no,))
        cur = cursor.fetchone() or {}
        current_status = cur.get("status")
        leave_type = cur.get("leave_type")
        used_count = cur.get("leave_number") or 0
        leave_dept = (cur.get("department") or "")

        email_query = f"""
            SELECT email
            FROM `{Config.MYSQL_DB2}`.`users`
            WHERE job_title = 'Department Head'
            AND department = %s
            AND email IS NOT NULL
            AND email <> ''
        """

        cursor.execute(email_query, (leave_dept,))
        rows = cursor.fetchall()

        depthead_emails = [r["email"] for r in rows if r.get("email")]

        

        detail_qry = f"""
            SELECT *,
                (SELECT d.department
                 FROM `{Config.MYSQL_DB2}`.departments d
                 WHERE d.dept_code = Leave_Details.department
                 LIMIT 1
                ) AS dept_code
            FROM Leave_Details
            LEFT JOIN `{Config.MYSQL_DB2}`.users
                ON Leave_Details.emp_id = ticketing_dev.users.emp_id
            WHERE ref_no = %s
        """

        department = (request.form.get("dept_code") or "").strip().upper()
        print("dept_code:", repr(department))

        cursor.execute("SELECT COUNT(*) as c FROM `{}`.`users`".format(Config.MYSQL_DB2))
        print("users count:", cursor.fetchone())

        cursor.execute(email_query, (department,))
        rows = cursor.fetchall() or []
        print("depthead rows:", rows)
        print("depthead_emails:", [r.get("email") for r in rows])


        # ✅ if already approved, don't recompute/update/history again
        if args == "APPROVED" and current_status == "APPROVED":
            if pdf_file:
                cursor.execute(detail_qry, (ref_no,))
                all_list = cursor.fetchone()
                send_vl_leave_request_email(
                    mail,
                    all_list['user'],
                    ref_no,
                    all_list['position'],
                    all_list['dept_code'],
                    all_list['leave_number'],
                    all_list['leave_from'],
                    all_list['leave_to'],
                    all_list['leave_reason'],
                    all_list['email'],
                    all_list['leave_type'],
                    depthead_emails=depthead_emails,
                    pdf_file=pdf_file
                )
            cursor.close()
            return jsonify({"success": True, "args": args, "already_approved": True}), 200

        # ✅ recompute only when not yet approved
        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_vl
            FROM Leave_Details
            WHERE emp_id = %s AND status = 'APPROVED' AND leave_type IN ('VL','EL')
        """, (emp_id,))
        used_vl = cursor.fetchone()["used_vl"]

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) as used_sl
            FROM Leave_Details
            WHERE emp_id = %s AND status = 'APPROVED' AND leave_type = 'SL'
        """, (emp_id,))
        used_sl = cursor.fetchone()["used_sl"]

        remaining_vl = max_leave - (used_vl + used_count)
        remaining_sl = max_leave - (used_sl + used_count)

        if args == "APPROVED":
            if leave_type == "SL":
                cursor.execute("""
                    UPDATE Leave_Details
                    SET status=%s, approved_by=%s, sl_remaining=%s, date_approved=NOW()
                    WHERE ref_no=%s
                """, (args, username, remaining_sl, ref_no))
            else:
                cursor.execute("""
                    UPDATE Leave_Details
                    SET status=%s, approved_by=%s, vl_remaining=%s, date_approved=NOW()
                    WHERE ref_no=%s
                """, (args, username, remaining_vl, ref_no))

            cursor.execute("""
                INSERT INTO leave_history (module, ref_no, action, `user`, history_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, ('LEAVE APPROVAL', ref_no, 'Approved Leave', username))

            mysql.connection.commit()

            cursor.execute("""
                SELECT status, approved_by, date_approved, vl_remaining, sl_remaining, leave_number, leave_type
                FROM Leave_Details
                WHERE ref_no = %s
                LIMIT 1
            """, (ref_no,))
            updated = cursor.fetchone() or {}

            if pdf_file:
                cursor.execute(detail_qry, (ref_no,))
                all_list = cursor.fetchone()
                send_vl_leave_request_email(
                    mail,
                    all_list['user'],
                    ref_no,
                    all_list['position'],
                    all_list['dept_code'],
                    all_list['leave_number'],
                    all_list['leave_from'],
                    all_list['leave_to'],
                    all_list['leave_reason'],
                    all_list['email'],
                    all_list['leave_type'],
                    depthead_emails=depthead_emails,
                    pdf_file=pdf_file
                )

            cursor.close()

            # ✅ RETURN HERE so frontend receives updated values
            return jsonify({
                "success": True,
                "args": args,
                "updated": updated,
                "already_approved": False
            }), 200

        elif args == "CANCELLED" :
            cursor.execute(
                "UPDATE  Leave_Details set status = %s WHERE ref_no = %s",(args, ref_no))
            
            cursor.execute(
                """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
                VALUES (%s, %s, %s, %s, NOW())""",
                ('CANCEL LEAVE', ref_no, 'Cancelled Leave', username)
            )
        else:
            cursor.execute(
                "UPDATE  Leave_Details set status = %s WHERE ref_no = %s",(args, ref_no))
            
            cursor.execute(
                """INSERT INTO leave_history (module, ref_no, action, `user`, history_date) 
                VALUES (%s, %s, %s, %s, NOW())""",
                ('LEAVE APPROVAL', ref_no, 'Denied Leave', username)
            )

        mysql.connection.commit()
        cursor.close()
        return jsonify({"success": True, "args": args, "leave_type": leave_type}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

@leave_bp.route('/date_calendar', methods=['POST'])
def get_calendar_date():
    try:
        data = request.get_json()
        department = data.get("dept_code")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT * 
            FROM Leave_Details 
            WHERE department = %s 
              AND status IN ("APPROVED","FOR DEPARTMENT HEAD APPROVAL")
        """, (department,))
        dateall = cursor.fetchall()

        cursor.execute("""
            SELECT * 
            FROM ot_ob 
            WHERE department = %s 
              AND status IN ("APPROVED","FOR DEPARTMENT HEAD APPROVAL")
        """, (department,))
        otoball = cursor.fetchall()

        # ✅ HOLIDAYS (MM-DD) ACTIVE only
        cursor.execute("""
            SELECT id, holiday_date, holiday_name, status
            FROM holidays
            WHERE status = 'ACTIVE'
        """)
        holidays = cursor.fetchall()

        cursor.close()

        return jsonify({
            "success": True,
            "dateall": dateall,
            "otoball": otoball,
            "holidays": holidays
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @leave_bp.route('/get_leaves_for_approval_request_date', methods=['POST'])
# def get_leaves_for_approval_request_date():
#     try:
#         data = request.get_json()
#         emp_id = data.get("emp_id")

#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("""
#             SELECT  leave_from,leave_to, leave_type from Leave_Details where emp_id = %s and (status = 'FOR DEPARTMENT HEAD APPROVAL' || status = 'APPROVED')
#         """, (emp_id,))  
#         alldates = cursor.fetchall()

#         cursor.close()

#         return jsonify({"success": True,"alldates":alldates}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}),500

@leave_bp.route('/get_leaves_for_approval_request_date', methods=['POST'])
def get_leaves_for_approval_request_date():
    try:
        expire_pending_vl()

        data = request.get_json()
        emp_id = data.get("emp_id")
        leave_type = data.get("leave_type")
        ref_no = data.get("ref_no")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            SELECT ref_no, leave_from, leave_to, leave_type, status
            FROM Leave_Details
            WHERE emp_id = %s AND status IN ('FOR DEPARTMENT HEAD APPROVAL', 'APPROVED')
        """, (emp_id,))
        alldates = cursor.fetchall()

        last_taken_ref = None

        if leave_type:
            # ✅ group VL + EL
            if leave_type in ("VL", "EL"):
                type_filter_sql = "AND leave_type IN ('VL','EL')"
                type_params = []
            else:
                type_filter_sql = "AND leave_type = %s"
                type_params = [leave_type]

            if ref_no:
                cursor.execute(f"""
                    SELECT ref_no
                    FROM Leave_Details
                    WHERE emp_id = %s
                      AND status = 'APPROVED'
                      {type_filter_sql}
                      AND ref_no <> %s
                    ORDER BY leave_to DESC
                    LIMIT 1
                """, tuple([emp_id] + type_params + [ref_no]))
            else:
                cursor.execute(f"""
                    SELECT ref_no
                    FROM Leave_Details
                    WHERE emp_id = %s
                      AND status = 'APPROVED'
                      {type_filter_sql}
                    ORDER BY leave_to DESC
                    LIMIT 1
                """, tuple([emp_id] + type_params))

            row = cursor.fetchone()
            last_taken_ref = row["ref_no"] if row else None

        cursor.close()

        return jsonify({
            "success": True,
            "alldates": alldates,
            "last_taken": last_taken_ref   
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@leave_bp.route('/update_denied_leaves', methods=['POST'])
def update_denied_leaves():
    try:
        data = request.get_json()
        ref_number = data.get("ref_number")
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        reason = data.get("leave_reason")
        leave_number = data.get("leave_number")
        fullName = data.get("fullName")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute("""
            UPDATE Leave_Details
            SET leave_from = %s,
                leave_to = %s,
                leave_reason = %s,
                leave_number = %s,
                status = %s,
                approved_by = NULL,
                date_approved = NULL
            WHERE ref_no = %s
        """, (date_from, date_to, reason, leave_number, "FOR DEPARTMENT HEAD APPROVAL", ref_number))

        cursor.execute("""
            INSERT INTO leave_history (module, ref_no, action, `user`, history_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, ('UPDATE LEAVE', ref_number, 'Updated denied leave and re-submitted for approval', fullName))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True}), 201
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500


@leave_bp.route('/get_remaining_leaves', methods=['POST'])
def get_remaining_leaves():
    try:
        data = request.get_json()
        emp_id = data.get("emp_id")

        ANNUAL_VL = 15
        ANNUAL_SL = 15

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # VL + EL share balance
        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) AS used_vl
            FROM Leave_Details
            WHERE emp_id = %s
              AND status = 'APPROVED'
              AND leave_type IN ('VL','EL')
        """, (emp_id,))
        used_vl = cursor.fetchone()["used_vl"]

        cursor.execute("""
            SELECT COALESCE(SUM(leave_number), 0) AS used_sl
            FROM Leave_Details
            WHERE emp_id = %s
              AND status = 'APPROVED'
              AND leave_type = 'SL'
        """, (emp_id,))
        used_sl = cursor.fetchone()["used_sl"]

        cursor.close()

        remaining_vl = max(ANNUAL_VL - used_vl, 0)
        remaining_sl = max(ANNUAL_SL - used_sl, 0)

        return jsonify({
            "success": True,
            "remaining": {
                "VL": remaining_vl,
                "SL": remaining_sl
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
