# db_ticketing.py
import MySQLdb  # type: ignore
from config import Config

def get_ticketing_conn():
    return MySQLdb.connect(
        host=Config.MYSQL_HOST2,        # Ensure the host is correct (e.g., 192.168.0.101)
        user=Config.MYSQL_USER,         # Correct user
        passwd=Config.MYSQL_PASSWORD,   # Correct password
        db=Config.MYSQL_DB2,            # Ensure this is set to 'central_dev'
        port=Config.MYSQL_PORT2,
        charset="utf8mb4",
    )