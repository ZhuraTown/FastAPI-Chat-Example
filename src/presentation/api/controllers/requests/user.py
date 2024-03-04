from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from transfer.user import ToCreateUserDTO


class RegisterUser(BaseModel):
    email: EmailStr
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)
    middle_name: Optional[str] = Field(None, max_length=64)
    password: str = Field(..., max_length=128)
    confirm_password: str = Field(..., max_length=128)

    def convert_to_dto(self) -> ToCreateUserDTO:
        return ToCreateUserDTO(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            password=self.password
        )
