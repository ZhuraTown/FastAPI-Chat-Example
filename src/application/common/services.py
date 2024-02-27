from abc import ABC
from typing import Generic, ParamSpec, TypeVar

# from application.common.uow import UnitOfWorkI

T = TypeVar('T')
Param = ParamSpec('Param')


class RepoService(Generic[T], ABC):
    def __init__(self, repository: T):
        self._repository: T = repository