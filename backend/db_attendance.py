# attendance.py
import MySQLdb  # type: ignore
from config import Config

def get_attendance_conn():
    return MySQLdb.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        passwd=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB1,
        port=Config.MYSQL_PORT,
        charset="utf8mb4",
    )
