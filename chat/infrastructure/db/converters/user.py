from infrastructure.db.models import User
from transfer.user import ToCreateUserDTO, UserDTO


def convert_user_dbmodel_to_dto(user: User) -> UserDTO | None:
    if not user:
        return

    return UserDTO(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        is_active=user.is_active,
        hashed_password=user.hashed_password,
        is_super_user=user.is_superuser
    )


def convert_created_user_to_dbmodel(user: ToCreateUserDTO, hash_password: str | None = None) -> User:
    user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
        is_active=True,
        is_superuser=False,
    )
    if hash_password:
        user.hashed_password = hash_password
    return user
