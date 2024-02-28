import asyncio

from application.services.user import UserService
from infrastructure.db.repositories.user import UserRepository
from faker import Faker

from transfer.user import ToCreateUserDTO


def user_service():
    return UserService(UserRepository())


async def main():
    faker_my = Faker("ru_RU")
    service_1 = user_service()

    # for i in range(0, 1000):
    #     data = ToCreateUserDTO(
    #         email=faker_my.email(),
    #         password="q123123123123123",
    #         first_name=faker_my.first_name(),
    #         last_name=faker_my.last_name(),
    #         middle_name=faker_my.middle_name()
    #     )
    #     await service_1.register_user(data)

    count = await service_1.get_users_count()
    users = await service_1.get_users(limit=100, offset=0, is_active=False)
    print(users)
    print(count)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)