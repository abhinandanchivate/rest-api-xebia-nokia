from app.repositories.user_repository import UserRepository
from app.models.user import User_tbl as User

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_id(self, user_id):
        return self.user_repository.get_by_id(user_id)

    def create_user(self, user: User):
        return self.user_repository.add(user)

    def update_user(self, user_id, updated_data: dict):
        return self.user_repository.update(user_id, updated_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    def search_user_by_email(self, email):
        return self.user_repository.search_by_email(email)

    def get_users_paginated(self, page=1, per_page=10):
        return self.user_repository.get_paginated(page, per_page)
