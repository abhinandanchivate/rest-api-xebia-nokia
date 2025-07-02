from app.repositories.asset_repository import AssetRepository
from app.models.asset import Asset

class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.asset_repository = asset_repository

    def get_all_assets(self):
        return self.asset_repository.get_all()

    def get_asset_by_id(self, asset_id):
        return self.asset_repository.get_by_id(asset_id)

    def create_asset(self, asset: Asset):
        return self.asset_repository.add(asset)

    def update_asset(self, asset_id, updated_data: dict):
        return self.asset_repository.update(asset_id, updated_data)

    def delete_asset(self, asset_id):
        return self.asset_repository.delete(asset_id)
