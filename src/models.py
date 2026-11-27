from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class IssueCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=2_000)
    priority: Literal["low", "medium", "high"]


class IssueResponse(BaseModel):
    id: str
    title: str
    description: str
    priority: Literal["low", "medium", "high"]
    status: Literal["open"]
    created_at: datetime


class IdempotencyRecord(BaseModel):
    request_hash: str
    issue: IssueResponse
