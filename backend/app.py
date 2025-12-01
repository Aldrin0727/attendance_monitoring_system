from flask import Flask, request, jsonify, session, g # type: ignore
from flask_cors import CORS # type: ignore
from flask_mysqldb import MySQL # type: ignore
import MySQLdb.cursors # type: ignore
from config import Config # type: ignore
from dotenv import load_dotenv # type: ignore

import os
import logging
from plugins import mysql  

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(Config)


CORS(app)
CORS(app, resources={r"/*": {"origins": "http://0.0.0.0"}}, supports_credentials=True)

mysql = MySQL(app)


logging.basicConfig(level=logging.INFO)

# Register blueprints
from models.Leaves import Leaves_bp
from models.user import users_bp

app.register_blueprint(Leaves_bp)
app.register_blueprint(users_bp)


def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connection
        except MySQLdb.OperationalError as e:
            if e.args[0] == 2006:  # MySQL server has gone away
                g.db = mysql.connection
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
    app.secret_key = os.getenv('SECRET_KEY', 'P@$$w0rD!!!')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000, debug=True)
