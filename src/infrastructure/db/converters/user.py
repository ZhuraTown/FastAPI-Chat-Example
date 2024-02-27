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
    )


def convert_created_user_to_dbmodel(user: ToCreateUserDTO) -> User:
    return User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        middle_name=user.middle_name,
    )

    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)