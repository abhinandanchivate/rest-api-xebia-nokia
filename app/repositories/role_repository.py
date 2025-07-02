import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.role import Role
from app.extensions import db

logger = logging.getLogger(__name__)

class RoleRepository:

    def get_all(self):
        try:
            return Role.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all roles: {e}")
            return []

    def get_by_id(self, role_id):
        try:
            return Role.query.get(role_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching role by ID {role_id}: {e}")
            return None

    def add(self, role):
        try:
            db.session.add(role)
            db.session.commit()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error adding role: {e}")
            return None

    def update(self, role_id, updated_data: dict):
        try:
            role = self.get_by_id(role_id)
            if not role:
                return None
            for key, value in updated_data.items():
                setattr(role, key, value)
            db.session.commit()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating role ID {role_id}: {e}")
            return None

    def delete(self, role_id):
        try:
            role = self.get_by_id(role_id)
            if role:
                db.session.delete(role)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting role ID {role_id}: {e}")
            return False
