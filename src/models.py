from typing import Literal

from pydantic import BaseModel, Field


class IssueCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2_000)
    priority: Literal["low", "medium", "high"]
