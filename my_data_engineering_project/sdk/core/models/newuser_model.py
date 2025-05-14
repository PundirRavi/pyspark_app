from pydantic import BaseModel, Field
from fastapi import Form

class NewUserRegisterRequest(BaseModel):
    username: str = Field(..., description="Username for the new user")
    password: str = Field(..., description="Password for the new user")
    email: str = Field(..., description="Email address of the new user")
    first_name: str = Field(..., description="First name of the new user")
    last_name: str = Field(..., description="Last name of the new user")
    phone_number: str = Field(..., description="Phone number of the new user")
    gender: str = Field(..., description="gender of the new user")
    date_of_birth: str = Field(..., description="Date of birth of the new user")

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        phone_number: str = Form(...),
        gender: str = Form(...),
        date_of_birth: str = Form(...),
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
        )
