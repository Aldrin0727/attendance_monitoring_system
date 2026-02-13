from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime
from config import Config
ot_ob_bp = Blueprint('ot_ob_bp', __name__)

from plugins import mail
from emails import send_otob_request_email, send_otob_for_approval_email, send_otob_for_final_approval_email,send_for_pre_approved_email

from datetime import datetime

def format_dt(val) -> str:
    if not val:
        return ""

    # if already datetime object
    if isinstance(val, datetime):
        return val.strftime("%b %d, %Y %I:%M %p")

    s = str(val).strip()

    formats = [
        "%Y-%m-%dT%H:%M",        # datetime-local
        "%Y-%m-%d %H:%M:%S",     # DB string
        "%Y-%m-%d %H:%M",        # sometimes no seconds
    ]

    for f in formats:
        try:
            dt = datetime.strptime(s, f)
            return dt.strftime("%b %d, %Y %I:%M %p")
        except Exception:
            pass

    return s  # last fallback


@ot_ob_bp.route('/create_ob_ot_request', methods=['POST'])
def create_request():
    try:
        data = request.get_json() or {}

        emp_id = data.get("emp_id")
        fullName = data.get("fullName")
        type = data.get("type")
        category = data.get("category")
        destination = data.get("destination")
        req_from = data.get("req_from")
        req_to = data.get("req_to")
        reason = data.get("reason")
        project = data.get("project")
        department = data.get("department")

        # ✅ shops from frontend (array)
        shops = data.get("shops") or []
        if not isinstance(shops, list):
            shops = []

        # ✅ validate + clean shops only if destination is Shops
        if destination == "Shops":
            cleaned = [str(s).strip() for s in shops if str(s).strip()]
            cleaned = sorted(set(cleaned), key=lambda x: x.lower())

            if len(cleaned) == 0:
                return jsonify({"success": False, "error": "Please select at least one shop."}), 400

            shops_str = ", ".join(cleaned)
        else:
            shops_str = None  # NULL/blank

        year = datetime.now().year
        ref_var = f"{type}{year}"

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT ref_number FROM ot_ob
            WHERE ref_number LIKE %s
            ORDER BY otob_id DESC LIMIT 1
        """, (ref_var + '%',))

        result = cursor.fetchone()
        if result and result.get("ref_number"):
            last_ref = result["ref_number"]
            ref_sequence = int(last_ref[-5:]) + 1
        else:
            ref_sequence = 1

        newref_No = f"{type}{year}{str(ref_sequence).zfill(5)}"

        # ✅ Insert
        cursor.execute("""
            INSERT INTO ot_ob (
              emp_id, fullName, type, category, destination,
              req_from, req_to, request_reason, project,
              date_created, status, ref_number, department, shop_location
            )
            VALUES (%s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    NOW(), %s, %s, %s, %s)
        """, (
            emp_id, fullName, type, category, destination,
            req_from, req_to, reason, project,
            "FOR PRE-APPROVAL", newref_No, department, shops_str
        ))

        cursor.execute("""
            INSERT INTO otob_history (module, ref_number, action, `user`, date)
            VALUES (%s, %s, %s, %s, NOW())
        """, ("OTOB SUBMITTED", newref_No, "New Request Has been submitted", fullName))

        # ✅ Get Dept Head emails (exclude requester)
        email_query = f"""
            SELECT email
            FROM `{Config.MYSQL_DB2}`.`users`
            WHERE job_title = 'Department Head'
              AND department = %s
              AND emp_id <> %s
              AND email IS NOT NULL
              AND email <> ''
        """
        cursor.execute(email_query, (department, emp_id))
        rows = cursor.fetchall() or []
        depthead_emails = [r["email"] for r in rows if r.get("email")]

        cursor.execute(f"""
                SELECT job_title
                FROM `{Config.MYSQL_DB2}`.users
                WHERE emp_id = %s
                LIMIT 1
            """, (emp_id,))
        u = cursor.fetchone() or {}
        requester_job_title = u.get("job_title") or ""

        mysql.connection.commit()
        cursor.close()

        # ✅ Send email AFTER commit (safe)
        if depthead_emails:
            send_otob_for_approval_email(
                mail=mail,
                dept_head_emails=depthead_emails,
                employee_name=fullName,
                ref_no=newref_No,
                dept=department,
                req_type=type,
                category=category,
                destination=destination,
                shop_location=shops_str,
                req_from=format_dt(req_from),
                req_to=format_dt(req_to),
                reason=reason,
                project=project,
                job_title=requester_job_title
            )

        return jsonify({"success": True, "ref_number": newref_No}), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"success": False, "error": str(e)}), 500



    
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

        if job_title == 'Department Head':
            base_query = f"""
                SELECT *
                FROM ot_ob
                LEFT JOIN `{Config.MYSQL_DB2}`.users
                ON ot_ob.emp_id = `{Config.MYSQL_DB2}`.users.emp_id
                WHERE ot_ob.status IN ('FOR PRE-APPROVAL', 'FOR FINAL APPROVAL')
                AND ot_ob.department = %s
            """
            values = [department]

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
        position = data.get("job_title")
        department = data.get("department")
        emp_id = data.get("emp_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # default values
        app_count = 0

        if position == "Department Head":
            cursor.execute("""
                SELECT COUNT(*) AS app_count
                FROM ot_ob
                WHERE department = %s
                  AND status IN ('FOR PRE-APPROVAL', 'FOR FINAL APPROVAL')
            """, (department,))
            app_count = cursor.fetchone()["app_count"]

        cursor.execute("""
            SELECT COUNT(*) AS otob_user_count
            FROM ot_ob
            WHERE emp_id = %s
              AND status IN ('FOR PRE-APPROVAL', 'FOR FINAL APPROVAL')
        """, (emp_id,))
        user_count = cursor.fetchone()["otob_user_count"]

        return jsonify({
            "app_count": app_count,
            "user_count": user_count,
            "success": True
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
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
        args = (request.form.get("args") or "").strip().upper()
        ref_number = (request.form.get("ref_number") or "").strip()
        username = (request.form.get("user") or "").strip()
        approver_emp_id = (request.form.get("emp_id") or "").strip()   # from frontend
        pdf_file = request.files.get("pdf")

        if not args or not ref_number:
            return jsonify({"success": False, "error": "Missing args or ref_number"}), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ get current status + requester
        cursor.execute("""
            SELECT status, emp_id, department
            FROM ot_ob
            WHERE ref_number = %s
            LIMIT 1
        """, (ref_number,))
        cur = cursor.fetchone() or {}

        if not cur:
            cursor.close()
            return jsonify({"success": False, "error": "Request not found"}), 404

        current_status = (cur.get("status") or "").strip().upper()
        requester_emp_id = cur.get("emp_id")
        dept_code = (cur.get("department") or "").strip()

        # ✅ block self-approval
        if args in ("PRE-APPROVED", "APPROVED") and requester_emp_id and approver_emp_id:
            if str(requester_emp_id) == str(approver_emp_id):
                cursor.close()
                return jsonify({
                    "success": False,
                    "error": "Self-approval is not allowed. Another Department Head must approve this request."
                }), 403

        # ✅ dept head emails (recipients for HR email copy)
        email_query = f"""
            SELECT email
            FROM `{Config.MYSQL_DB2}`.`users`
            WHERE job_title = 'Department Head'
              AND department = %s
              AND email IS NOT NULL
              AND email <> ''
        """
        cursor.execute(email_query, (dept_code,))
        rows = cursor.fetchall() or []
        depthead_emails = [r["email"] for r in rows if r.get("email")]

        # ✅ If already approved and frontend calls again with PDF, just send email w/ PDF (NO DB update)
        # This supports your 2-step flow:
        #   1) call endpoint w/out pdf to update DB
        #   2) generate pdf then call again with pdf
        if args == "APPROVED" and current_status == "APPROVED":
            if pdf_file:
                cursor.execute(f"""
                    SELECT
                      ot_ob.*,
                      u.email,
                      u.contact,
                      u.address,
                      u.position,
                      (SELECT d.department
                        FROM `{Config.MYSQL_DB2}`.departments d
                        WHERE d.dept_code = ot_ob.department
                        LIMIT 1
                      ) AS dept_name
                    FROM ot_ob
                    LEFT JOIN `{Config.MYSQL_DB2}`.users u
                      ON ot_ob.emp_id = u.emp_id
                    WHERE ot_ob.ref_number = %s
                    LIMIT 1
                """, (ref_number,))
                otob = cursor.fetchone() or {}

                send_otob_request_email(
                    mail=mail,
                    user=otob.get("fullName"),
                    ref_no=otob.get("ref_number"),
                    dept=otob.get("dept_name") or otob.get("department"),
                    req_type=otob.get("type"),
                    category=otob.get("category"),
                    destination=otob.get("destination"),
                    shop_location=otob.get("shop_location"),
                    req_from=format_dt(otob.get("req_from")),
                    req_to=format_dt(otob.get("req_to")),
                    actual_from=format_dt(otob.get("actual_from")),
                    actual_to=format_dt(otob.get("actual_to")),
                    actual_hours=otob.get("actual_hours"),
                    employee_email=otob.get("email"),
                    depthead_emails=depthead_emails,
                    pdf_file=pdf_file
                )

            # return latest status fields
            cursor.execute("""
                SELECT status, approved_by, date_approved, preapproved_by, date_preapproved
                FROM ot_ob
                WHERE ref_number = %s
                LIMIT 1
            """, (ref_number,))
            row = cursor.fetchone() or {}
            cursor.close()

            return jsonify({
                "success": True,
                "args": args,
                "already_approved": True,
                "status": row.get("status"),
                "approved_by": row.get("approved_by"),
                "date_approved": str(row.get("date_approved")) if row.get("date_approved") else None,
                "preapproved_by": row.get("preapproved_by"),
                "date_preapproved": str(row.get("date_preapproved")) if row.get("date_preapproved") else None,
            }), 200

        # ✅ NORMAL UPDATE FLOW
        if args == "APPROVED":
            cursor.execute("""
                UPDATE ot_ob
                SET status=%s, approved_by=%s, date_approved=NOW()
                WHERE ref_number=%s
            """, ("APPROVED", username, ref_number))

            cursor.execute("""
                INSERT INTO otob_history (module, ref_number, action, `user`, date)
                VALUES (%s, %s, %s, %s, NOW())
            """, ('REQUEST APPROVAL', ref_number, 'Approved Request', username))

            mysql.connection.commit()

            # ✅ refetch updated details (for email + response)
            cursor.execute(f"""
                SELECT
                  ot_ob.*,
                  u.email,
                  u.contact,
                  u.address,
                  u.position,
                  (SELECT d.department
                    FROM `{Config.MYSQL_DB2}`.departments d
                    WHERE d.dept_code = ot_ob.department
                    LIMIT 1
                  ) AS dept_name
                FROM ot_ob
                LEFT JOIN `{Config.MYSQL_DB2}`.users u
                  ON ot_ob.emp_id = u.emp_id
                WHERE ot_ob.ref_number = %s
                LIMIT 1
            """, (ref_number,))
            otob = cursor.fetchone() or {}

            # ✅ send after commit
            if pdf_file:
                send_otob_request_email(
                    mail=mail,
                    user=otob.get("fullName"),
                    ref_no=otob.get("ref_number"),
                    dept=otob.get("dept_name") or otob.get("department"),
                    req_type=otob.get("type"),
                    category=otob.get("category"),
                    destination=otob.get("destination"),
                    shop_location=otob.get("shop_location"),
                    req_from=format_dt(otob.get("req_from")),
                    req_to=format_dt(otob.get("req_to")),
                    actual_from=format_dt(otob.get("actual_from")),
                    actual_to=format_dt(otob.get("actual_to")),
                    actual_hours=otob.get("actual_hours"),
                    employee_email=otob.get("email"),
                    depthead_emails=depthead_emails,
                    pdf_file=pdf_file
                )

            cursor.close()
            return jsonify({
                "success": True,
                "args": args,
                "already_approved": False,
                "status": otob.get("status"),
                "approved_by": otob.get("approved_by"),
                "date_approved": str(otob.get("date_approved")) if otob.get("date_approved") else None,
            }), 200

        elif args == "PRE-APPROVED":
            cursor.execute("""
                UPDATE ot_ob
                SET status=%s, preapproved_by=%s, date_preapproved=NOW()
                WHERE ref_number=%s
            """, ("PRE-APPROVED", username, ref_number))

            cursor.execute("""
                INSERT INTO otob_history (module, ref_number, action, `user`, date)
                VALUES (%s, %s, %s, %s, NOW())
            """, ('REQUEST APPROVAL', ref_number, 'Pre-approved Request', username))

            mysql.connection.commit()

            cursor.execute("""
                SELECT status, preapproved_by, date_preapproved
                FROM ot_ob
                WHERE ref_number = %s
                LIMIT 1
            """, (ref_number,))
            row = cursor.fetchone() or {}

            # ✅ refetch updated details (for email + response)
            cursor.execute(f"""
                SELECT
                  ot_ob.*,
                  u.email,
                  u.contact,
                  u.address,
                  u.position,
                  (SELECT d.department
                    FROM `{Config.MYSQL_DB2}`.departments d
                    WHERE d.dept_code = ot_ob.department
                    LIMIT 1
                  ) AS dept_name
                FROM ot_ob
                LEFT JOIN `{Config.MYSQL_DB2}`.users u
                  ON ot_ob.emp_id = u.emp_id
                WHERE ot_ob.ref_number = %s
                LIMIT 1
            """, (ref_number,))
            otob = cursor.fetchone() or {}

            # ✅ send after commit
 
            send_for_pre_approved_email(
                    mail=mail,
                    user=otob.get("fullName"),
                    ref_no=otob.get("ref_number"),
                    dept=otob.get("dept_name") or otob.get("department"),
                    req_type=otob.get("type"),
                    category=otob.get("category"),
                    destination=otob.get("destination"),
                    shop_location=otob.get("shop_location"),
                    req_from=format_dt(otob.get("req_from")),
                    req_to=format_dt(otob.get("req_to")),
                    actual_from=format_dt(otob.get("actual_from")),
                    actual_to=format_dt(otob.get("actual_to")),
                    actual_hours=otob.get("actual_hours"),
                    employee_email=otob.get("email"),
                    project=otob.get("project"),
                    reason=otob.get("request_reason"),

                    depthead_emails=depthead_emails,
                )
            
            cursor.close()

            return jsonify({
                "success": True,
                "args": args,
                "status": row.get("status"),
                "preapproved_by": row.get("preapproved_by"),
                "date_preapproved": str(row.get("date_preapproved")) if row.get("date_preapproved") else None,
            }), 200

        else:
            # DENIED / CANCELLED / etc.
            cursor.execute("""
                UPDATE ot_ob
                SET status=%s
                WHERE ref_number=%s
            """, (args, ref_number))

            cursor.execute("""
                INSERT INTO otob_history (module, ref_number, action, `user`, date)
                VALUES (%s, %s, %s, %s, NOW())
            """, ('REQUEST APPROVAL', ref_number, f'{args.title()} Request', username))

            mysql.connection.commit()

            cursor.execute("""
                SELECT status
                FROM ot_ob
                WHERE ref_number = %s
                LIMIT 1
            """, (ref_number,))
            row = cursor.fetchone() or {}
            cursor.close()

            return jsonify({
                "success": True,
                "args": args,
                "status": row.get("status"),
            }), 200

    except Exception as e:
        try:
            mysql.connection.rollback()
        except Exception:
            pass
        return jsonify({"success": False, "error": str(e)}), 500

    
@ot_ob_bp.route('/update_actual_date', methods=['POST'])
def update_actual_date():
    try:
        data = request.get_json() or {}

        ref_number = data.get("ref_number")
        actual_from = data.get("actual_from")
        actual_to = data.get("actual_to")
        actual_hours = data.get("actual_hours")
        fullName = data.get("user")
        approver_emp_id = data.get("emp_id") 

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ update to FOR FINAL APPROVAL
        cursor.execute("""
            UPDATE ot_ob
            SET actual_from=%s, actual_to=%s, actual_hours=%s, status=%s
            WHERE ref_number=%s
        """, (actual_from, actual_to, actual_hours, "FOR FINAL APPROVAL", ref_number))

        cursor.execute("""
            INSERT INTO otob_history (module, ref_number, action, `user`, date)
            VALUES (%s, %s, %s, %s, NOW())
        """, ('ACTUAL REQUEST', ref_number, 'Update Actual Date and Time', fullName))

        # ✅ pull details for email + get dept heads
        cursor.execute(f"""
            SELECT
              ot_ob.*,
              (SELECT d.department
               FROM `{Config.MYSQL_DB2}`.departments d
               WHERE d.dept_code = ot_ob.department
               LIMIT 1
              ) AS dept_name
            FROM ot_ob
            WHERE ot_ob.ref_number = %s
            LIMIT 1
        """, (ref_number,))
        otob_details = cursor.fetchone() or {}

        dept_code = (otob_details.get("department") or "").strip()
        req_type = otob_details.get("type")
        category = otob_details.get("category")
        destination = otob_details.get("destination")
        shop_location = otob_details.get("shop_location")
        reason = otob_details.get("request_reason")
        project = otob_details.get("project")
        employee_name = otob_details.get("fullName")
        dept_name = otob_details.get("dept_name") or dept_code
        requester_emp_id = otob_details.get("emp_id")
        req_from_db = otob_details.get("req_from")
        req_to_db = otob_details.get("req_to")
        req_email = otob_details.get("email")

        # ✅ dept head emails (exclude requester)
        email_query = f"""
            SELECT email
            FROM `{Config.MYSQL_DB2}`.`users`
            WHERE job_title = 'Department Head'
              AND department = %s
              AND emp_id <> %s
              AND email IS NOT NULL
              AND email <> ''
        """
        cursor.execute(email_query, (dept_code, requester_emp_id))
        rows = cursor.fetchall() or []
        depthead_emails = [r["email"] for r in rows if r.get("email")]

        cursor.execute(f"""
                SELECT job_title
                FROM `{Config.MYSQL_DB2}`.users
                WHERE emp_id = %s
                LIMIT 1
            """, (requester_emp_id,))
        u = cursor.fetchone() or {}
        requester_job_title = u.get("job_title") or ""

        mysql.connection.commit()
        cursor.close()

        # ✅ send final approval email after commit
        if depthead_emails:
            send_otob_for_final_approval_email(
                mail=mail,
                dept_head_emails=depthead_emails,
                employee_name=employee_name,
                ref_no=ref_number,
                dept=dept_name,
                req_type=req_type,
                category=category,
                destination=destination,
                shop_location=shop_location,
                req_from=format_dt(req_from_db),
                req_to=format_dt(req_to_db),
                actual_from=format_dt(actual_from),
                actual_to=format_dt(actual_to),
                actual_hours=actual_hours,
                reason=reason,
                project=project,
                req_email=req_email,
                job_title=requester_job_title
            )

        return jsonify({"success": True, "ref_no": ref_number}), 201

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"error": str(e)}), 500

    
@ot_ob_bp.route('/get_otob_for_approval_request_date', methods=['POST'])
def get_otob_for_approval_request_date():
    try:
        data = request.get_json()
        emp_id = data.get("emp_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT  * from ot_ob where emp_id = %s and (status = 'FOR PRE-APPROVAL' || status = 'APPROVED' || status = 'FOR FINAL APPROVAL')
        """, (emp_id,))  
        alldates = cursor.fetchall()

        cursor.close()

        return jsonify({"success": True,"alldates":alldates}), 201
    except Exception as e:
        return jsonify({"error": str(e)}),500

@ot_ob_bp.route('/depthead_all_otob', methods=['POST'])
def depthead_all_otob():
    try:
        data = request.get_json() or {}

        dept_code = (data.get("dept_code") or "").strip()
        status = (data.get("status") or "").strip()
        req_type = (data.get("type") or "").strip()          # "OT" or "OB"
        category = (data.get("category") or "").strip()

        viewer_emp_id = (data.get("emp_id") or "").strip()   # optional but recommended

        if not dept_code:
            return jsonify({"success": False, "error": "dept_code is required"}), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # ✅ verify Dept Head (using DB2 users)
        if viewer_emp_id:
            cursor.execute(f"""
                SELECT job_title
                FROM `{Config.MYSQL_DB2}`.users
                WHERE emp_id = %s
                LIMIT 1
            """, (viewer_emp_id,))
            u = cursor.fetchone() or {}
            if u.get("job_title") != "Department Head":
                cursor.close()
                return jsonify({"success": False, "error": "Unauthorized"}), 403

        base_query = f"""
            SELECT
              ot_ob.*,
              u.email,
              u.first_name,
              u.last_name,
              u.job_title,
              u.contact,
              u.address,
              u.position,
              (SELECT d.department
                FROM `{Config.MYSQL_DB2}`.departments d
                WHERE d.dept_code = ot_ob.department
                LIMIT 1
              ) AS dept_name
            FROM ot_ob
            LEFT JOIN `{Config.MYSQL_DB2}`.users u
              ON ot_ob.emp_id = u.emp_id
            WHERE ot_ob.department = %s
        """
        values = [dept_code]

        # ✅ optional filters
        if status:
            base_query += " AND ot_ob.status = %s"
            values.append(status)

        if req_type:
            base_query += " AND ot_ob.type = %s"
            values.append(req_type)

        if category:
            base_query += " AND ot_ob.category = %s"
            values.append(category)

        base_query += " ORDER BY ot_ob.date_created DESC"

        cursor.execute(base_query, tuple(values))
        all_list = cursor.fetchall() or []

        cursor.close()
        return jsonify({"success": True, "all_list": all_list}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
