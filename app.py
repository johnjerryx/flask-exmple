from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect
import os
import jwt
from urllib.parse import quote_plus
from utils import extract_app_token

if os.getenv("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    if os.getenv("FLASK_ENV") == 'local':
        load_dotenv('.env.local', override=True)
    else:
        load_dotenv()

csrf: CSRFProtect = CSRFProtect()
db: SQLAlchemy = SQLAlchemy()
login_manager: LoginManager = LoginManager()


def create_app():
    
    app = Flask(__name__, template_folder='templates')

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql://{os.getenv('MYSQL_USER')}:"
        f"{quote_plus(os.getenv('MYSQL_PASSWORD'))}"
        f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/"
        f"{os.getenv('MYSQL_DB')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    csrf.init_app(app)
    db.init_app(app)
    

    login_manager.init_app(app)
    login_manager.login_view = 'user_login_get'

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return db.session.get(User, int(uid))
    
    bcrypt = Bcrypt(app)


    @app.before_request
    def verify_is_our_app():

        if not request.path.startswith('/api'):
            return

        client_token = extract_app_token(request.headers.get("X-Auth", ""))

        if not client_token:
            return jsonify({"error": "Unauthorized action."}), 401
        
        try:
            jwt.decode(client_token, app.config["APP_VERIFICATION_SECRET"], algorithms=["HS256"])
        except jwt.PyJWTError:
            return jsonify({"error": "Unauthorized action."}), 401
    
    from routes import register_routes
    register_routes(app, db, bcrypt)

    Migrate(app, db)

    return app