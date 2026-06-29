from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime,date
from config import Config

attendance_bp = Blueprint('attendance_bp', __name__)
from datetime import datetime
from datetime import datetime

@attendance_bp.route('/time_check', methods=['POST'])
def insert_time():
    try:
        data = request.get_json()
        username = data.get("fullName")
        emp_id = data.get("emp_id")
        time_in = data.get("time_in") or ""
        time_out = data.get("time_out") or ""
        args = data.get("args")

        fmt = "%Y-%m-%d %H:%M:%S"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # If the action is 'TIME IN'
        if args == "TIME IN":
            if not time_in:
                return jsonify({"error": "Time In cannot be empty"}), 400

            start = datetime.strptime(time_in, fmt)
            # Get the date part of time_in
            time_in_date = start.date().strftime("%Y-%m-%d") 

            # Check if the time is considered late
            if (start.hour >= 10 and start.minute > 0 and start.hour <= 12) or (start.hour >= 14 and start.minute > 0):
                remarks = "LATE"
            else:
                remarks = ""

            # Check if the user has already recorded Time In for today
            cursor.execute("""
                SELECT count(*) as timein_today FROM attendance 
                WHERE emp_id = %s AND time_in LIKE %s
            """, (emp_id, time_in_date + "%"))
            
            timein_today = cursor.fetchone()["timein_today"]

            if timein_today < 1:
                cursor.execute(
                    "INSERT INTO attendance (`emp_id`, full_name, time_in, date_encoded, remarks) "
                    "VALUES (%s, %s, %s, NOW(), %s)",
                    (emp_id, username, time_in, remarks)
                )
                mysql.connection.commit()

        # If the action is 'TIME OUT'
        else:
            if not time_out:
                return jsonify({"error": "Time Out cannot be empty"}), 400

            end = datetime.strptime(time_out, fmt)
            time_out_date = end.date().strftime("%Y-%m-%d")

            # Fetch the 'Time In' record for the same date as the 'Time Out'
            cursor.execute("""
                SELECT time_in FROM attendance 
                WHERE emp_id = %s AND time_in LIKE %s
            """, (emp_id, time_out_date + "%"))

            time_in_record = cursor.fetchone()

            if time_in_record:
                # Retrieve the 'Time In' from the database and convert it to datetime
                time_in_record_str = time_in_record["time_in"]
                
            if time_in_record:
                # Check if time_in_record["time_in"] is already a datetime object or string
                time_in_record_str = time_in_record["time_in"]

                # If it's already a datetime object, no need to use strptime
                if isinstance(time_in_record_str, datetime):
                    time_in_record_dt = time_in_record_str
                else:
                    # If it's a string, then convert it into datetime
                    time_in_record_dt = datetime.strptime(time_in_record_str, fmt)

                # Now, time_in_record_dt is the start time (Time In)
                # Calculate work hours
                work_hours = calculate_work_hours(time_in_record_dt, end)
                #Calculate if HALFDAY, OVERTIME, UNDERTIME OR NO REMARKS
                remarks = remarks_undertime(time_in_record_dt, end)

                # Fetch the 'Time In' record for the same date as the 'Time Out'
                cursor.execute("""
                    SELECT remarks FROM attendance 
                    WHERE emp_id = %s AND time_in LIKE %s
                """, (emp_id, time_out_date + "%"))

                remarks_from_db = cursor.fetchone()["remarks"]

                status = f"{remarks_from_db}{","}{remarks}"

                # Update the 'Time Out' and work hours in the database
                cursor.execute(
                    "UPDATE attendance SET time_out = %s, work_hours = %s,remarks = %s WHERE emp_id = %s AND time_in  = %s",
                    (time_out, work_hours, status, emp_id, time_in_record_str)
                )
                mysql.connection.commit()

                return jsonify({
                    "success": True,
                    "time_in": time_in_record_dt.strftime(fmt),
                    "time_out": time_out,
                    "work_hours": work_hours,
                    "remarks" : remarks
                }), 201

            else:
                return jsonify({"error": "No matching Time In record found for the selected date"}), 400


        cursor.close()
        return jsonify({"success": True, "remarks": remarks}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to calculate work hours and subtract 1 hour for lunch break
def calculate_work_hours(time_in_record_dt, end):
    # Calculate the difference between time_in and time_out
    diff = end - time_in_record_dt
    total_seconds = diff.total_seconds()

    # Calculate the total hours and minutes
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    # Subtract 1 hour for the lunch break (3600 seconds)
    total_seconds -= 3600  # Subtracting 1 hour (lunch break)

    # Recalculate hours and minutes after subtracting the lunch break
    if total_seconds < 0:
        total_seconds = 0  # Ensure the total time doesn't go negative

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    # Format the work hours as a string
    return f"{hours} hrs {minutes} min(s)" 

def remarks_undertime(time_in_record_dt, end):
    # Calculate the difference between time_in and time_out
    diff = end - time_in_record_dt
    total_seconds = diff.total_seconds()

    # Calculate the total hours and minutes
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    # Subtract 1 hour for the lunch break (3600 seconds)
    if time_in_record_dt.hour >= 13 or  (time_in_record_dt.hour <= 14 and time_in_record_dt.minute == 0) :
        total_seconds = total_seconds  # Subtracting 1 hour (lunch break)
    elif time_in_record_dt.hour <= 9 and end.hour <=14:
        total_seconds = total_seconds  # Subtracting 1 hour (lunch break)
    else:
        total_seconds -= 3600  # Subtracting 1 hour (lunch break)

    # Recalculate hours and minutes after subtracting the lunch break
    if total_seconds < 0:
        total_seconds = 0  # Ensure the total time doesn't go negative

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    if time_in_record_dt.hour >= 13 or  (time_in_record_dt.hour <= 14 and time_in_record_dt.minute == 0) :
        if hours <= 3:
            return "UNDERTIME, HALFDAY"
        else:
            return "HALFDAY"
    elif time_in_record_dt.hour <= 9 and end.hour <=14:
        if hours <= 3:
            return "UNDERTIME, HALFDAY"
        else:
            return "HALFDAY"
    else:
        if hours < 7 :
            return "UNDERTIME"
        elif hours > 8 :
            return "OVERTIME"
        else :
            return ""
    
@attendance_bp.route('/check_attendance_by_emp', methods=['POST'])
def get_list_of_attendance():  
    try:
        data = request.get_json()
        emp_id = data.get("emp_id")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        attendance_qry = f"""
                       SELECT * from attendance where emp_id = %s"""
        values = [emp_id] 
        cursor.execute(attendance_qry, tuple(values))
        alllist = cursor.fetchall()
        cursor.close()

        return jsonify({"success": True,"alllist":alllist}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


