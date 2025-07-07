# # from functools import wraps
# # from flask_jwt_extended import get_jwt_identity
# # from flask import jsonify
# # from app.services.user_service import UserService
# # from flask_injector import inject
# # @inject
# # def permission_required(*actions: str, require_all: bool = False,user_service:UserService):
# #     """
# #     Decorator to check if a user has one or more permissions.
    
# #     Usage:
# #     @permission_required("create", "update")  # any of these
# #     @permission_required("create", "update", require_all=True)  # all required
# #     """
# #     def decorator(fn):
# #         @wraps(fn)
# #         def wrapper(*args, **kwargs):
# #             identity = get_jwt_identity()
# #             user = user_service.get_user_by_id(identity)

# #             if not user:
# #                 return jsonify({"error": "User not found"}), 404

# #             if not user.role or not user.role.permissions:
# #                 return jsonify({"error": "No permissions assigned to role"}), 403

# #             permissions = user.role.permissions

# #             if require_all:
# #                 # Must have ALL specified permissions
# #                 if not all(permissions.get(action, False) for action in actions):
# #                     return jsonify({"error": f"Missing one or more required permissions: {actions}"}), 403
# #             else:
# #                 # Must have AT LEAST ONE of the permissions
# #                 if not any(permissions.get(action, False) for action in actions):
# #                     return jsonify({"error": f"Permission denied. Required any of: {actions}"}), 403

# #             return fn(*args, **kwargs)
# #         return wrapper
# #     return decorator

# from functools import wraps
# from flask_jwt_extended import get_jwt_identity
# from flask import jsonify
# from app.services.user_service import UserService

# def permission_required(*actions: str, require_all: bool = False):
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             identity = get_jwt_identity()
#             user_service = UserService()
#             user = user_service.get_user_by_id(identity)

#             if not user:
#                 return jsonify({"error": "User not found"}), 404

#             if not user.role or not user.role.permissions:
#                 return jsonify({"error": "No permissions assigned to role"}), 403

#             permissions = user.role.permissions

#             if require_all:
#                 if not all(permissions.get(action, False) for action in actions):
#                     return jsonify({"error": f"Missing one or more required permissions: {actions}"}), 403
#             else:
#                 if not any(permissions.get(action, False) for action in actions):
#                     return jsonify({"error": f"Missing required permission for any of: {actions}"}), 403

#             return fn(*args, **kwargs)
#         return wrapper
#     return decorator

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.services.user_service import UserService

def permission_required(*actions: str, require_all: bool = False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()

            # Expecting DI to inject `user_service` as a kwarg
            user_service: UserService = kwargs.get("user_service")
            if not user_service:
                return jsonify({"error": "Internal error: UserService not injected"}), 500

            user = user_service.get_user_by_id(identity)
            if not user:
                return jsonify({"error": "User not found"}), 404

            if not user.role or not user.role.permissions:
                return jsonify({"error": "No permissions assigned to role"}), 403

            permissions = user.role.permissions

            if require_all:
                if not all(permissions.get(action, False) for action in actions):
                    return jsonify({"error": f"Missing one or more required permissions: {actions}"}), 403
            else:
                if not any(permissions.get(action, False) for action in actions):
                    return jsonify({"error": f"Missing required permission for any of: {actions}"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
