from dataclasses import dataclass

from application.common.exceptions import ToClientException


@dataclass(eq=False)
class UserWithEmailAlreadyExists(ToClientException):
    email: str

    @property
    def message(self):
        return f"User with email {self.email} already exists"

