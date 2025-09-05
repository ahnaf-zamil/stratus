"""
Contains validation schemas for API requests
"""

from pydantic import BaseModel, Field, AnyHttpUrl


class CreateApplicationRequest(BaseModel):
    name: str = Field(max_length=50, min_length=3)
    """Application name"""

    runtime: str = Field(min_length=3)
    """Application runtime ID e.g py310"""

    git_repo: AnyHttpUrl
    """Remote Git repo to fetch application code from"""
