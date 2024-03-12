from abc import ABC
from typing import Generic, ParamSpec, TypeVar

# from application.common.uow import UnitOfWorkI
from application.common.uow import UnitOfWorkI

T = TypeVar('T')
Param = ParamSpec('Param')


class RepoService(Generic[T], ABC):
    def __init__(self, repository: T):
        self._repository: T = repository


class UowRepoService(Generic[T], RepoService[T]):
    def __init__(self, uow: UnitOfWorkI, *args: Param.args, **kwargs: Param.kwargs):
        super().__init__(*args, **kwargs)
        self._uow: UnitOfWorkI = uow
