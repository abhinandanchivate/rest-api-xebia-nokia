from app.repositories.role_repository import RoleRepository
from app.models.role import Role

class RoleService:
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository

    def get_all_roles(self):
        return self.role_repository.get_all()

    def get_role_by_id(self, role_id):
        return self.role_repository.get_by_id(role_id)

    def create_role(self, role: Role):
        return self.role_repository.add(role)

    def update_role(self, role_id, updated_data: dict):
        return self.role_repository.update(role_id, updated_data)

    def delete_role(self, role_id):
        return self.role_repository.delete(role_id)
