from flask import Blueprint, jsonify, request
from app.services.UserService import UserService
from app.exceptions import AppException, UserNotFoundError, UserAlreadyExistsError, ValidationError

user_bp = Blueprint("users", __name__)


@user_bp.route("", methods=["GET"])
def get_all_users():
    """Get all users"""
    try:
        users = UserService.get_all_users()
        return jsonify({
            "success": True,
            "data": users,
            "count": len(users)
        }), 200
    except AppException as e:
        return jsonify({
            "success": False,
            "error": e.message
        }), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a user by ID"""
    try:
        user = UserService.get_user_by_id(user_id)
        return jsonify({
            "success": True,
            "data": user
        }), 200
    except AppException as e:
        return jsonify({
            "success": False,
            "error": e.message
        }), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500


@user_bp.route("", methods=["POST"])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("No data provided")
        
        username = data.get("username")
        if not username:
            raise ValidationError("Username is required")
        
        bio = data.get("bio")
        birth_year = data.get("birth_year")
        
        user = UserService.create_user(
            username=username,
            bio=bio,
            birth_year=birth_year
        )
        
        return jsonify({
            "success": True,
            "data": user,
            "message": "User created successfully"
        }), 201
    except AppException as e:
        return jsonify({
            "success": False,
            "error": e.message
        }), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500


@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a user by ID"""
    try:
        data = request.get_json()
        
        if not data:
            raise ValidationError("No data provided")
        
        username = data.get("username")
        bio = data.get("bio")
        birth_year = data.get("birth_year")
        
        user = UserService.update_user(
            user_id=user_id,
            username=username,
            bio=bio,
            birth_year=birth_year
        )
        
        return jsonify({
            "success": True,
            "data": user,
            "message": "User updated successfully"
        }), 200
    except AppException as e:
        return jsonify({
            "success": False,
            "error": e.message
        }), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a user by ID"""
    try:
        UserService.delete_user(user_id)
        return jsonify({
            "success": True,
            "message": "User deleted successfully"
        }), 200
    except AppException as e:
        return jsonify({
            "success": False,
            "error": e.message
        }), e.status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred"
        }), 500
