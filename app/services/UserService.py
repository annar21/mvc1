from app.db import get_db
from app.exceptions import UserNotFoundError, UserAlreadyExistsError, DatabaseError

class UserService:
    @staticmethod
    def create_user(username, bio=None, birth_year=None):
        """Create a new user"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (username, bio, birth_year) VALUES (?, ?, ?)",
                (username, bio, birth_year)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            # Fetch the created user
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = dict(cursor.fetchone())
            return user
        except Exception as e:
            conn.rollback()
            error_message = str(e)
            if "UNIQUE constraint" in error_message or "UNIQUE constraint failed" in error_message:
                raise UserAlreadyExistsError(username)
            raise DatabaseError(f"Failed to create user: {error_message}")
        finally:
            conn.close()
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users ORDER BY id")
            users = [dict(row) for row in cursor.fetchall()]
            return users
        finally:
            conn.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get a user by ID"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if not row:
                raise UserNotFoundError(user_id)
            return dict(row)
        except UserNotFoundError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get user: {str(e)}")
        finally:
            conn.close()
    
    @staticmethod
    def update_user(user_id, username=None, bio=None, birth_year=None):
        """Update a user by ID"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # Check if user exists first
            UserService.get_user_by_id(user_id)
            
            # Build update query dynamically based on provided fields
            updates = []
            params = []
            
            if username is not None:
                updates.append("username = ?")
                params.append(username)
            if bio is not None:
                updates.append("bio = ?")
                params.append(bio)
            if birth_year is not None:
                updates.append("birth_year = ?")
                params.append(birth_year)
            
            if not updates:
                # No fields to update, return current user
                return UserService.get_user_by_id(user_id)
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            
            # Fetch the updated user
            return UserService.get_user_by_id(user_id)
        except UserNotFoundError:
            raise
        except UserAlreadyExistsError:
            raise
        except Exception as e:
            conn.rollback()
            error_message = str(e)
            if "UNIQUE constraint" in error_message or "UNIQUE constraint failed" in error_message:
                raise UserAlreadyExistsError(username)
            raise DatabaseError(f"Failed to update user: {error_message}")
        finally:
            conn.close()
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user by ID"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # Check if user exists first
            UserService.get_user_by_id(user_id)
            
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except UserNotFoundError:
            raise
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"Failed to delete user: {str(e)}")
        finally:
            conn.close()

