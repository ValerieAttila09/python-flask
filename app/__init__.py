from flask import Flask
from flask_login import LoginManager
from .models import User
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .main import main_bp
    app.register_blueprint(main_bp)

    return app
