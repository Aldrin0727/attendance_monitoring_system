from flask import Flask, request, jsonify, session, g 
from flask_cors import CORS
from flask_mysqldb import MySQL # type: ignore
import MySQLdb.cursors
from config import Config
from dotenv import load_dotenv
import os
import logging
from flask_cors import cross_origin # type: ignore

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(Config)

CORS(app)
mysql = MySQL(app)

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Register blueprints
from models.create_leave import create_leave_bp

app.register_blueprint(create_leave_bp)

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connection
        except MySQLdb.OperationalError as e:
            if e.args[0] == 2006:  # MySQL server has gone away
                g.db = mysql.connection  # Reconnect
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal Server Error: {error}")
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(404)
def not_found(error):
    app.logger.warning(f"Not Found: {error}")
    return jsonify({"error": "Not Found"}), 404
    
if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY', 'P@$$w0rD!!!')  # Use environment variable for production
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='localhost', port=5000, debug=True)
    # app.run(host='192.168.0.101', port=5000, debug=True)
