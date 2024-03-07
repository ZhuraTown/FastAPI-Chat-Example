from fastapi_filter.contrib.sqlalchemy import Filter

from infrastructure.db.models import User


class UserFilter(Filter):
    name__in = ...

    class Constans(Filter.Constants):
        model = User

    class Config:
        allow_population_by_field_name = True
