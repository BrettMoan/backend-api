# FastAPI Serverless Tasks API Boilerplate

This app demonstrates a serverless backend using FastAPI, DynamoDB, and AWS Lambda, with async event processing (SQS/EventBridge ready).

## Features
- CRUD endpoints for tasks
- Soft delete (tasks are hidden but not removed)
- Async event trigger endpoint (stub for SQS/EventBridge)
- DynamoDB integration
- Pydantic models for validation
- IaaC ready (Terraform example below)

## Endpoints
- `POST /tasks` — Create a new task
- `GET /tasks` — List all tasks (excluding deleted)
- `GET /tasks/{id}` — Get a specific task
- `PUT /tasks/{id}` — Update a task (partial update)
- `DELETE /tasks/{id}` — Soft delete a task
- `POST /tasks/{id}/trigger` — Trigger async event for a task

## DynamoDB Table (Terraform)
```
resource "aws_dynamodb_table" "tasks" {
  name           = "tasks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Environment = "dev"
  }
}
```

## Local Development
- Install dependencies: `uv pip install -r pyproject.toml --extra local`
- Run: `python -m uvicorn backend_api.main:app --reload`
- Set AWS credentials and region in your environment for DynamoDB access

## Deployment
- Use Terraform to provision DynamoDB, Lambda, API Gateway, SQS/EventBridge
- Deploy FastAPI app as Lambda using Mangum

---
This boilerplate is designed for AWS free tier and can be extended for more complex demos.
