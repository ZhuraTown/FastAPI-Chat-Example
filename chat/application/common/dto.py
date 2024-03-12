from abc import ABC
from typing import Any, Hashable

from application.common.constants import Empty


class DTO(ABC):
    """
    Base DTO class has implementation keys and __getitem__ for using unpacking.
    """

    def keys(self) -> set[Hashable]:
        return {k for k, v in self.__dict__.items() if v is not Empty.UNSET}

    def __getitem__(self, item) -> Any:
        return self.__dict__[item]