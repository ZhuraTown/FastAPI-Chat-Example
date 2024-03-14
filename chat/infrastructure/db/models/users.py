from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from chat.infrastructure.db.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

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
    # is admin??
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))
    middle_name: Mapped[str | None] = mapped_column(String(64), nullable=True)

    def __repr__(self):
        return (
            f'<User id={self.id},'
            f' email={self.email},'
            f' first_name={self.first_name},'
            f' last_name={self.last_name},'
        )


# engine = create_async_engine(str(settings.infrastructure.postgres_dsn))
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)