from pydantic import BaseModel, Field
from fastapi import Form
from typing import Annotated

class loginRequest(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")

    @classmethod
    def as_form(
        cls,
        username: Annotated[str, Form(...)] = None,
        password: Annotated[str, Form(...)] = None
    ) -> "loginRequest":
        return cls(username=username, password=password)
