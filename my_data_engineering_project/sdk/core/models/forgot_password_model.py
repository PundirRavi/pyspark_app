from pydantic import BaseModel, Field
from fastapi import Form

class forgotPasswordRequest(BaseModel):
    username: str = Field(..., description="Registered username")
    gender: str = Field(..., description="Gender of the user")
    date_of_birth: str = Field(..., description="Date of birth of the user in YYYY-MM-DD format")

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        gender: str = Form(...),
        date_of_birth: str = Form(...),
    ):
        return cls(username=username, gender=gender, date_of_birth=date_of_birth)
