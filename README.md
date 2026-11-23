# Retry-Safe Issue Service

A FastAPI service that safely handles retried issue-creation requests using idempotency keys.

## Problem

Clients may retry an API request after a timeout, network failure, or uncertain response. Without protection, a retry can create duplicate issues.

## Goal

Build a REST API that creates and retrieves issues while ensuring that repeated requests with the same idempotency key do not create duplicate records.

## Core Requirements

- Create an issue
- Retrieve an issue by ID
- Accept an `Idempotency-Key` request header for issue creation
- Return the original issue for a repeated request using the same key
- Reject reuse of an idempotency key when the request content is different
- Store issues and idempotency records in a database
- Include unit and integration tests
- Document API behavior and failure cases

## Example API Request

```http
POST /issues
Idempotency-Key: 8f7c4e0a-example-key
Content-Type: application/json
```

```json
{
  "title": "Login failure",
  "description": "The user receives an error after submitting credentials.",
  "priority": "high"
}
```
