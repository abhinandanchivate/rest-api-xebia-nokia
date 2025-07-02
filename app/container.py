from flask_injector import FlaskInjector
from injector import Binder, singleton

# Repositories
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.asset_repository import AssetRepository

# Services
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.asset_service import AssetService

def configure(binder: Binder):
    # Bind repositories as singletons
    binder.bind(UserRepository, to=UserRepository(), scope=singleton)
    binder.bind(RoleRepository, to=RoleRepository(), scope=singleton)
    binder.bind(AssetRepository, to=AssetRepository(), scope=singleton)

    # Bind services as singletons (with DI)
    binder.bind(UserService, to=UserService(binder.injector.get(UserRepository)), scope=singleton)
    binder.bind(RoleService, to=RoleService(binder.injector.get(RoleRepository)), scope=singleton)
    binder.bind(AssetService, to=AssetService(binder.injector.get(AssetRepository)), scope=singleton)

def setup_di(app):
    FlaskInjector(app=app, modules=[configure])
