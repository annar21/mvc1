from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.users import users_bp 
    app.register_blueprint(users_bp, url_prefix="/users")

    return app