from pydantic import BaseModel, Field


class CreateApplicationRequest(BaseModel):
    name: str = Field(max_length=50, min_length=3)
    runtime: str = Field(min_length=3)
