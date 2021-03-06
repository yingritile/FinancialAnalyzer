"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser, sys

config = configparser.ConfigParser()
config.read("app/FinancialAnalyzer.ini")

if len(sys.argv) > 1 and sys.argv[1] == "PROD":
    app_url = config['PROD'].get('url', "192.168.0.14")
    app_port = config['PROD'].get('port', '5000')
else:
    app_url = config['LOCAL'].get('url', "127.0.0.1")
    app_port = config['LOCAL'].get('port', '5000')

db_config = config['MYSQL_DB']
db_user = db_config.get('user', 'root')
db_pwd = db_config.get('pwd', 'root')
db_url = db_config.get('url', '127.0.0.1')
db_port = db_config.get('port', '8889')
db_database = db_config.get('database', 'FinancialAnalyzer')

db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    """Construct the core application."""
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + db_user + ":" + db_pwd + "@" + db_url + ":" + db_port + "/" + db_database
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['SECRET_KEY'] = 'DontTellAnyone'
    app.config['BASE_FOLDER'] = sys.path[0]

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        db.create_all()  # Create database tables for our data models

        return app