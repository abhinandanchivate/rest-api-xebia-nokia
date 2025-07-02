import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.extensions import db

logger = logging.getLogger(__name__)

class UserRepository:

    def get_all(self):
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all users: {e}")
            return []

    def get_by_id(self, user_id):
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            return None

    def add(self, user):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error adding user {user}: {e}")
            return None

    def update(self, user_id, updated_data: dict):
        try:
            user = self.get_by_id(user_id)
            if not user:
                return None
            for key, value in updated_data.items():
                setattr(user, key, value)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating user ID {user_id}: {e}")
            return None

    def delete(self, user_id):
        try:
            user = self.get_by_id(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting user ID {user_id}: {e}")
            return False

    def search_by_email(self, email):
        try:
            return User.query.filter_by(email=email).first()
        except SQLAlchemyError as e:
            logger.error(f"Error searching user by email {email}: {e}")
            return None

    def get_paginated(self, page: int = 1, per_page: int = 10):
        try:
            return User.query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching paginated users: {e}")
            return []
