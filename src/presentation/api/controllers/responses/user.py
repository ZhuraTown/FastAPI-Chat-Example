from typing import Self, Optional
from uuid import UUID

from src.presentation.api.controllers.responses import BaseResponse
from transfer.user import UserDTO


class UserResponse(BaseResponse):
    id: UUID
    email: str
    first_name: str
    last_name: str
    middle_name: str | None = None

    @classmethod
    def convert_from_dto(cls, dto: UserDTO) -> Self:
        return cls(
            id=dto.id,
            email=dto.email,
            first_name=dto.first_name,
            last_name=dto.last_name,
            middle_name=dto.middle_name,
            is_active=True
        )
