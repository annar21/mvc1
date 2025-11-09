class AppException(Exception):
    """Base exception class for the application"""
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundError(AppException):
    """Raised when a user is not found"""
    def __init__(self, user_id=None):
        message = f"User not found"
        if user_id:
            message = f"User with id {user_id} not found"
        super().__init__(message, status_code=404)


class UserAlreadyExistsError(AppException):
    """Raised when trying to create a user with an existing username"""
    def __init__(self, username):
        message = f"User with username '{username}' already exists"
        super().__init__(message, status_code=409)


class ValidationError(AppException):
    """Raised when validation fails"""
    def __init__(self, message):
        super().__init__(message, status_code=400)


class DatabaseError(AppException):
    """Raised when a database operation fails"""
    def __init__(self, message="Database operation failed"):
        super().__init__(message, status_code=500)

