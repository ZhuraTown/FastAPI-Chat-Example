from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Self

from pydantic import BaseModel

from application.common.dto import DTO

_DT = TypeVar("_DT", bound=DTO)


class BaseResponse(ABC, BaseModel, Generic[_DT]):

    @abstractmethod
    def convert_from_dto(self, dto: _DT) -> Self: pass