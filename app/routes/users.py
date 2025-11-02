from flask import Blueprint, jsonify, request
from app.services.UserService import create_user as cu
# from app.controllers.UsersController import create_user as cu

users_bp = Blueprint("users",__name__)



@users_bp.route("/create", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)
    usr, pwd = data.get('username'), data.get("password")
    if not usr or not pwd:
        return {"error": "Incorrect request data!"}, 400

    try:
        user = cu(usr=usr, pwd=pwd)
    except Exception as e:
        print(e)
        return {"error": "some error"}, 400

    return jsonify(user), 201