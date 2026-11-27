from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status

from src.models import IssueCreate, IssueResponse


app = FastAPI(
    title="Retry-Safe Issue Service",
    version="0.1.0",
)

# Temporary in-memory storage for the learning MVP.
# This data disappears whenever the API service restarts.
issues: dict[str, IssueResponse] = {}

# Maps an Idempotency-Key value to the first issue created with that key.
# We will later store a request hash here to detect conflicting key reuse.
idempotency_records: dict[str, IssueResponse] = {}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a basic indication that the API process is responding."""
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
    # A repeated key returns the original issue instead of creating a duplicate.
    existing_issue = idempotency_records.get(idempotency_key)

    if existing_issue is not None:
        return existing_issue

    # Server-managed fields prevent clients from controlling IDs or timestamps.
    created_issue = IssueResponse(
        id=str(uuid4()),
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status="open",
        created_at=datetime.now(timezone.utc),
    )

    # Store the issue by its server-generated ID for GET /issues/{issue_id}.
    issues[created_issue.id] = created_issue

    # Store the original result under the request key for safe client retries.
    idempotency_records[idempotency_key] = created_issue

    return created_issue


@app.get("/issues/{issue_id}")
def get_issue(issue_id: str) -> IssueResponse:
    """Return a stored issue or a clear 404 response when it does not exist."""
    saved_issue = issues.get(issue_id)

    if saved_issue is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found",
        )

    return saved_issue
