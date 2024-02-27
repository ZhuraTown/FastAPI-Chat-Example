from infrastructure.db.repositories.user import UserRepository
from src.application.common.services import RepoService


class UserService(RepoService[UserRepository]):

    def register_user(self, data):
        ...

    def update_user(self, user_id, data):
        ...

    def get_user_by_id(self, user_id):
        ...

    def get_users(self, filters):
        ...

    def reset_password(self, user_id, old_password, new_password):
        ...
