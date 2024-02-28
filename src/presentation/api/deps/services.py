import asyncio

from application.services.user import UserService
from infrastructure.db.repositories.user import UserRepository
from faker import Faker

from transfer.user import ToCreateUserDTO


def user_service():
    return UserService(UserRepository())


async def main():
    service_1 = user_service()
    # count = await service_1.get_users_count()
    # users = await service_1.get_users(limit=100, offset=0, is_active=False)
    user_id = "e1903418-0bb8-45c4-bdb1-19327e465d0c"
    user = await service_1.get_user_by_id(user_id=user_id)
    await service_1.deactivate_user(user.id)
    print(user)
    # print(users)
    # print(count)


if __name__ == "__main__":
    asyncio.run(main())