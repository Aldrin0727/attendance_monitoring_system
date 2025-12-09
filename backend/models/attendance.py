from flask import Blueprint, request, jsonify, session  # type: ignore
import MySQLdb.cursors                                 # type: ignore
from plugins import mysql 
from datetime import datetime
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
        time_in = data.get("time_in")
        time_out = data.get("time_out")

        if not time_in:
            return jsonify({"error": "Time In cannot be empty"}), 400

        fmt = "%Y-%m-%d %H:%M:%S"

        try:
            start = datetime.strptime(time_in, fmt)
        except ValueError:
            return jsonify({"error": f"Invalid Time In format. Expected format is '{fmt}'"}), 400

        # If time_out is not provided, set it to null or skip calculations
        if time_out:
            try:
                end = datetime.strptime(time_out, fmt)
            except ValueError:
                return jsonify({"error": f"Invalid Time Out format. Expected format is '{fmt}'"}), 400

            # Calculate work hours if both time_in and time_out are provided
            diff = end - start
            total_seconds = diff.total_seconds()
            diffhours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
    
            work_hours = f"{diffhours} hrs {minutes} mins"
        else:
            work_hours = "Not yet marked"  # If time_out is null, you can set a placeholder

        # Insert the record into the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "INSERT INTO attendance (`emp_id`, full_name, time_in, time_out, date_encoded, work_hours) "
            "VALUES (%s, %s, %s, %s, NOW(), %s)",
            (emp_id, username, time_in, time_out if time_out else None, work_hours)
        )

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            "success": True,
            "interval": work_hours,
            "specific": start.minute
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
