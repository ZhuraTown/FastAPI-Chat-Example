from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from application.services.user import UserService
from presentation.api.controllers.requests.user import RegisterUser
from presentation.api.controllers.responses.user import UserResponse
from presentation.api.deps.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_user(
        new_user: RegisterUser,
        service: Annotated[UserService, Depends(user_service)]
) -> UserResponse:
    created_user = await service.register_user(data=new_user.convert_to_dto())
    return UserResponse.convert_from_dto(created_user)


# TODO: register user

# todo: get_users

# todo: get_me

# todo: update_me

# todo: update_user

# todo: deactivate_user

