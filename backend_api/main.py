"""
Docstring for backend_api.main
"""
import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend_api.models import Task, TaskUpdate
from backend_api.db import tasks_table

app = FastAPI()

# Enable CORS for all origins (adjust as needed for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## we wouldn't do this in prod, but for demo purposes we can just serve the docs as the root
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/docs")

@app.get("/favicon.ico")
def favicon():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "favicon.ico"))

# Create a new task
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskUpdate):
    now = datetime.now(timezone.utc).isoformat()
    item = {
        "id": str(uuid.uuid4()),
        "title": task.title or "Untitled",
        "description": task.description,
        "status": task.status or "pending",
        "created_at": now,
        "updated_at": now,
        "tags": task.tags or [],
        "metadata": task.metadata or {},
        "deleted": False,
        "deleted_at": None
    }
    tasks_table.put_item(Item=item)
    return item

# List all tasks (excluding deleted)
@app.get("/tasks", response_model=List[Task])
def list_tasks(status: Optional[str] = None):
    scan_kwargs = {
        "FilterExpression": "deleted = :d",
        "ExpressionAttributeValues": {":d": False}
    }
    if status:
        scan_kwargs["FilterExpression"] += " AND #st = :s"
        scan_kwargs.setdefault("ExpressionAttributeNames", {})["#st"] = "status"
        scan_kwargs["ExpressionAttributeValues"][":s"] = status
    # DynamoDB doesn't support contains in FilterExpression for lists in scan, so we skip tag filtering for demo simplicity
    response = tasks_table.scan(**scan_kwargs)
    return response.get("Items", [])

# Get a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    response = tasks_table.get_item(Key={"id": task_id})
    item = response.get("Item")
    if not item or item.get("deleted"):
        raise HTTPException(status_code=404, detail="Task not found")
    return item

# Update a task (partial update)
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, update: TaskUpdate):
    response = tasks_table.get_item(Key={"id": task_id})
    item = response.get("Item")
    if not item or item.get("deleted"):
        raise HTTPException(status_code=404, detail="Task not found")
    updated = item.copy()
    for field, value in update.model_dump(exclude_unset=True).items():
        updated[field] = value
    updated["updated_at"] = datetime.now(timezone.utc).isoformat()
    tasks_table.put_item(Item=updated)
    return updated

# Soft delete a task
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: str):
    response = tasks_table.get_item(Key={"id": task_id})
    item = response.get("Item")
    if not item or item.get("deleted"):
        raise HTTPException(status_code=404, detail="Task not found")
    item["deleted"] = True
    item["deleted_at"] = datetime.now(timezone.utc).isoformat()
    item["updated_at"] = item["deleted_at"]
    tasks_table.put_item(Item=item)
    return item

# Trigger async event (stub for SQS/EventBridge integration)
@app.post("/tasks/{task_id}/trigger", status_code=status.HTTP_202_ACCEPTED)
def trigger_task_event(task_id: str):
    response = tasks_table.get_item(Key={"id": task_id})
    item = response.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Task not found")
    # TODO: send a message to SQS/EventBridge
    # For demo, just return accepted
    return {"message": f"Async event triggered for task {task_id}"}
