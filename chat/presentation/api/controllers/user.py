from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from application.services.interfaces.user import UserServiceI
from presentation.api.controllers.requests.user import (
    RegisterUser,
    UserUpdateRequest)
from presentation.api.controllers.responses import (
    LimitOffsetPaginator,
    lo_paginator,
    PaginatedResponse)
from presentation.api.controllers.responses.user import UserDetailResponse
from presentation.api.deps.services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    name="register user",
    response_model=UserDetailResponse
)
async def register_user(
        new_user: RegisterUser,
        service: Annotated[UserServiceI, Depends(user_service)]
) -> UserDetailResponse:
    created_user = await service.register_user(data=new_user.convert_to_dto())
    return UserDetailResponse.convert_from_dto(created_user)


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailResponse,
)
async def get_user_details(
        user_id: UUID,
        # todo: add # auth_user
        service: Annotated[UserServiceI, Depends(user_service)]
) -> UserDetailResponse:
    user = await service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return UserDetailResponse.convert_from_dto(user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(
        user_id: UUID,
        # todo: add # auth_user
        service: Annotated[UserServiceI, Depends(user_service)]
):
    # todo: add check user self or admin
    user = await service.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.deactivate_user(user_id)


@router.get("",
            status_code=status.HTTP_200_OK,
            name="get users"
            )
async def get_users(
        paginator: Annotated[LimitOffsetPaginator[UserDetailResponse], Depends(lo_paginator)],
        service: Annotated[UserServiceI, Depends(user_service)],
        is_active: bool = True,
) -> PaginatedResponse[UserDetailResponse]:
    users = await service.get_users(
        limit=paginator.limit,
        offset=paginator.offset,
        is_active=is_active,
    )
    count = await service.get_users_count(is_active=is_active)
    return paginator.paginate(users, count, model=UserDetailResponse)


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    name="update user",
    response_model=UserDetailResponse
)
async def update_user(
        user_id: UUID,
        update_data: UserUpdateRequest,
        service: Annotated[UserServiceI, Depends(user_service)]
):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await service.update_user(user, update_data.dict())


