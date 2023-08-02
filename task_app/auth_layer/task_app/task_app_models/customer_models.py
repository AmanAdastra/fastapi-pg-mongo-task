from pydantic import EmailStr, BaseModel, validator
from typing import Any


class UserRegisterRequest(BaseModel):
    fullname: str
    email: EmailStr
    phone: str
    password: str

    @validator("phone")
    def validate_mobile_number(cls, value):
        if len(value) != 12:
            raise ValueError("Phone Number Must Be Twelve Digits")
        if not str(value).startswith("91"):
            raise ValueError("Phone Number Must Start with 91")
        if not str(value).isnumeric():
            raise ValueError("Phone Number Must Be Numeric")
        return value

    @validator("fullname")
    def validate_full_name(cls, value):
        if len(value) > 50:
            raise ValueError("Please enter a valid name less than 50 Characters")
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "johndoe",
                "phone": "919999999999",
                "email": "johndoe@mailinator.com",
                "password": "Test@123",
            }
        }


class ResponseMessage(BaseModel):
    type: str
    data: Any
    status_code: int
