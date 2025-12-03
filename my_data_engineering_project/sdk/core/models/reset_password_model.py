from pydantic import BaseModel, Field, field_validator
from fastapi import Form

class ResetPasswordRequest(BaseModel):
    username: str = Field(..., description="Username for password reset")
    new_password: str = Field(..., min_length=6, description="New password")
    confirm_password: str = Field(..., min_length=6, description="Confirm new password")

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, confirm_password, values):
        if "new_password" in values and confirm_password != values["new_password"]:
            raise ValueError("Passwords do not match")
        return confirm_password

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        new_password: str = Form(...),
        confirm_password: str = Form(...)
    ):
        return cls(
            username=username,
            new_password=new_password,
            confirm_password=confirm_password
        )
