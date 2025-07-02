import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.asset import Asset
from app.extensions import db

logger = logging.getLogger(__name__)

class AssetRepository:

    def get_all(self):
        try:
            return Asset.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching all assets: {e}")
            return []

    def get_by_id(self, asset_id):
        try:
            return Asset.query.get(asset_id)
        except SQLAlchemyError as e:
            logger.error(f"Error fetching asset by ID {asset_id}: {e}")
            return None

    def add(self, asset):
        try:
            db.session.add(asset)
            db.session.commit()
            return asset
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error adding asset: {e}")
            return None

    def update(self, asset_id, updated_data: dict):
        try:
            asset = self.get_by_id(asset_id)
            if not asset:
                return None
            for key, value in updated_data.items():
                setattr(asset, key, value)
            db.session.commit()
            return asset
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error updating asset ID {asset_id}: {e}")
            return None

    def delete(self, asset_id):
        try:
            asset = self.get_by_id(asset_id)
            if asset:
                db.session.delete(asset)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error deleting asset ID {asset_id}: {e}")
            return False
