from flask import Blueprint, request, jsonify, session # type: ignore
from config import Config
from plugins import mysql 
import MySQLdb.cursors # type: ignore
from flask_mysqldb import MySQL # type: ignore

holidays_bp = Blueprint('holidays', __name__)

from datetime import datetime

@holidays_bp.route("/add_holiday", methods=["POST"])
def add_holiday():
    data = request.get_json()
    holiday_date = (data.get("holiday_date") or "").strip()
    holiday_name = (data.get("holiday_name") or "").strip()
    status = (data.get("status") or "ACTIVE").strip()
    created_by = (data.get("created_by") or "").strip()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        INSERT INTO holidays (holiday_date, holiday_name, status, created_by, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, (holiday_date, holiday_name, status, created_by))
    holiday_id = cursor.lastrowid
    
    cursor.execute("""
            INSERT INTO holidays_history (holiday_id, module, action, `user`, history_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (holiday_id, "HOLIDAY", f"Added holiday: {holiday_name} ({holiday_date})", created_by))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True}), 201


@holidays_bp.route("/holidays_list", methods=["POST"])
def list_holidays():
    try:
        data = request.get_json(silent=True) or {}
        year = data.get("year")                 # optional (e.g. 2026)
        # active_only = data.get("active_only", 1)  # default: active lang

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        qry = """
            SELECT id,
                   holiday_date,
                   holiday_name,
                   status,
                   created_at
            FROM holidays
            WHERE 1=1
        """
        params = []

        qry += " ORDER BY holiday_date ASC"

        cursor.execute(qry, tuple(params))
        rows = cursor.fetchall()
        cursor.close()

        return jsonify({"success": True, "holidays": rows}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@holidays_bp.route("/update_holiday", methods=["POST"])
def update_holiday():
    try:
        data = request.get_json()
        hid = data.get("id")
        new_name = (data.get("holiday_name") or "").strip()
        new_date = (data.get("holiday_date") or "").strip()   # MM-DD
        new_status = (data.get("status") or "").strip()
        updated_by = (data.get("updated_by") or "").strip()

        if not hid or not new_name or not new_date or not new_status:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # 1) get old row
        cursor.execute("SELECT * FROM holidays WHERE id = %s LIMIT 1", (hid,))
        old = cursor.fetchone()
        if not old:
            cursor.close()
            return jsonify({"success": False, "error": "Holiday not found"}), 404

        old_name = (old.get("holiday_name") or "").strip()
        old_date = (old.get("holiday_date") or "").strip()
        old_status = (old.get("status") or "").strip()

        # 2) build diff action (only changes)
        changes = []
        if old_name != new_name:
            changes.append(f"Name: '{old_name}' → '{new_name}'")
        if old_date != new_date:
            changes.append(f"Date: {old_date} → {new_date}")
        if old_status != new_status:
            changes.append(f"Status: {old_status} → {new_status}")

        if not changes:
            cursor.close()
            return jsonify({"success": True, "message": "No changes detected"}), 200

        action = "Updated holiday: " + ", ".join(changes)

        # 3) update holidays
        cursor.execute("""
            UPDATE holidays
            SET holiday_name = %s,
                holiday_date = %s,
                status = %s,
                created_by = %s,
                created_at = NOW()
            WHERE id = %s
        """, (new_name, new_date, new_status, updated_by, hid))

        # 4) insert history
        cursor.execute("""
            INSERT INTO holidays_history (holiday_id, module, action, `user`, history_date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (hid, "HOLIDAY", action, updated_by))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True}), 200

    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
