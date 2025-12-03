from pydantic import BaseModel, Field
from fastapi import Form
from typing import Optional
from datetime import datetime, timezone

class NewUserRegisterRequest(BaseModel):
    username: str = Field(..., description="Username for the new user")
    password: str = Field(..., description="Password for the new user")
    email: Optional[str] = Field(..., description="Email address of the new user")
    first_name: str = Field(..., description="First name of the new user")
    last_name: str = Field(..., description="Last name of the new user")
    phone_number: Optional[str] = Field(..., description="Phone number of the new user")
    gender: str = Field(..., description="gender of the new user")
    date_of_birth: str = Field(..., description="Date of birth of the new user")
    created_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_on: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = Field(..., description="last login datetime")
    isActive: bool = Field(default=True, description="Is the user active?")
    isDeleted: bool = Field(default=False, description="Is the user deleted?")

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        email: Optional[str] = Form(None),
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone_number: Optional[str] = Form(None),
        gender: str = Form(...),
        date_of_birth: str = Form(...),
        last_login: Optional[datetime] = Form(None),
        isActive: bool = Form(default=True),
        isDeleted: bool = Form(default=False)
    ):
        return cls(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
            date_of_birth=date_of_birth,
            last_login=last_login,
            isActive=isActive,
            isDeleted=isDeleted
        )
