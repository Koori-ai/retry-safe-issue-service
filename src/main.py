import hashlib
import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status

from src.models import IdempotencyRecord, IssueCreate, IssueResponse


app = FastAPI(
    title="Retry-Safe Issue Service",
    version="0.1.0",
)

issues: dict[str, IssueResponse] = {}
idempotency_records: dict[str, IdempotencyRecord] = {}


def calculate_request_hash(issue: IssueCreate) -> str:
    request_data = {
        "title": issue.title,
        "description": issue.description,
        "priority": issue.priority,
    }
    canonical_request = json.dumps(
        request_data,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()


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
    request_hash = calculate_request_hash(issue)
    existing_record = idempotency_records.get(idempotency_key)

    if existing_record is not None:
        if existing_record.request_hash != request_hash:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Idempotency-Key has already been used with different request data",
            )

        return existing_record.issue

    created_issue = IssueResponse(
        id=str(uuid4()),
        title=issue.title,
        description=issue.description,
        priority=issue.priority,
        status="open",
        created_at=datetime.now(timezone.utc),
    )

    issues[created_issue.id] = created_issue
    idempotency_records[idempotency_key] = IdempotencyRecord(
        request_hash=request_hash,
        issue=created_issue,
    )

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
