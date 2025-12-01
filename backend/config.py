import os
from dotenv import load_dotenv #type: ignore
load_dotenv()

class Config:
    # MYSQL_HOST = '192.168.0.237'
    # MYSQL_USER = 'root'
    # MYSQL_PASSWORD = 'cosmic020486'
    # MYSQL_DB = 'attendace_system' 
    # MYSQL_PORT = 3306

#     MYSQL_HOST = os.getenv('MYSQL_HOST')
#     MYSQL_USER = os.getenv('MYSQL_USER')
#     MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
#     MYSQL_DB = os.getenv('MYSQL_DB')

#     # Flask-Mail Configuration
#     MAIL_SERVER = 'smtp.gmail.com'  # Use Gmail's SMTP server
#     MAIL_PORT = 465  # Use SSL port (465)
#     MAIL_USE_TLS = False  # Disable TLS since you're using SSL
#     MAIL_USE_SSL = True  # Use SSL for secure connection
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # Your Gmail username
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Use the application-specific password here
#     MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # Default sender email

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')