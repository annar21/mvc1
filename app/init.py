from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.controllers.UserController import user_bp
    
    app.register_blueprint(user_bp, url_prefix="/users")

    return app