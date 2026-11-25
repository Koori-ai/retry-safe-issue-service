from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, status

from src.models import IssueCreate, IssueResponse


app = FastAPI(
    title="Retry-Safe Issue Service",
    version="0.1.0",
)

issues: dict[str, IssueResponse] = {}

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_issue(issue: IssueCreate) -> IssueResponse:
    created_issue = IssueResponse(
        id=str(uuid4()),
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status="open",
        created_at=datetime.now(timezone.utc),
    )

    issues[created_issue.id] = created_issue

    return created_issue
