from typing import Optional

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    root_validator
)

from transfer.user import ToCreateUserDTO, UpdatedUserData


class RegisterUser(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)
    middle_name: Optional[str] = Field(None, max_length=64)
    password: str = Field(..., max_length=128, min_length=8)
    confirm_password: str = Field(..., max_length=128)

    def convert_to_dto(self) -> ToCreateUserDTO:
        return ToCreateUserDTO(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            password=self.password
        )

    @root_validator(pre=True)
    def verify_password_match(cls, values):
        pw1, pw2 = values.get('password'), values.get('confirm_password')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('Пароли не совпадают!')
        return values


class UserUpdateRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)
    middle_name: Optional[str] = Field(None, max_length=64)

    def typed_dict(self) -> UpdatedUserData:
        return self.dict()
