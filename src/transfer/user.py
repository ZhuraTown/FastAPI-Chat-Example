from dataclasses import dataclass
from uuid import UUID

from application.common.dto import DTO


@dataclass(frozen=True)
class ToCreateUserDTO(DTO):
    email: str
    first_name: str
    last_name: str
    middle_name: str | None
    password: str


@dataclass(frozen=True)
class UserDTO(DTO):
    id: UUID
    email: str
    first_name: str
    last_name: str
    middle_name: str | None
    is_active: bool  # todo: ??

    def __repr__(self) -> str:
        return (
            f'<User: '
            f'id={self.id}, '
            f'email={self.email}, '
            f'first_name={self.first_name}, '
            f'last_name={self.last_name}>'
        )