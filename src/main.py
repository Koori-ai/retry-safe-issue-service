from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status

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
def create_issue(
    issue: IssueCreate,
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> IssueResponse:
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


@app.get("/issues/{issue_id}")
def get_issue(issue_id: str) -> IssueResponse:
    saved_issue = issues.get(issue_id)

    if saved_issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found",
        )

    return saved_issue
