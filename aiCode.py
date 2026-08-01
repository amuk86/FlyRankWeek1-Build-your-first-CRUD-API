"""
Task CRUD API
Generated from prompt (Stage 7 - AI Rematch)

Run with:
    python -m uvicorn main:app --port 8000 --reload

Swagger UI available at:
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Task API",
    description="A simple in-memory CRUD API for managing tasks.",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# In-memory storage
# ---------------------------------------------------------------------------

tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
    {"id": 3, "title": "Task 3", "done": False},
]

next_id = 4  # tracks the next id to assign on create


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Task title, cannot be empty")
    done: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="New title (optional)")
    done: Optional[bool] = Field(None, description="New done status (optional)")


class Task(BaseModel):
    id: int
    title: str
    done: bool


# ---------------------------------------------------------------------------
# Root & health endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Meta"])
def index():
    """Basic hello-world root endpoint."""
    return {"message": "Hello World!"}


@app.get("/health", tags=["Meta"])
def health():
    """Simple health check endpoint."""
    return {"status": "OK"}


# ---------------------------------------------------------------------------
# GET /tasks  and  GET /tasks/{id}
# ---------------------------------------------------------------------------

@app.get("/tasks", response_model=list[Task], tags=["Tasks"])
def get_tasks():
    """Return the full list of tasks."""
    return tasks


@app.get("/tasks/{id}", response_model=Task, tags=["Tasks"])
def get_task(id: int):
    """Return a single task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


# ---------------------------------------------------------------------------
# POST /tasks
# ---------------------------------------------------------------------------

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task_in: TaskCreate):
    """
    Create a new task.
    - title is required and cannot be empty (enforced by Pydantic Field)
    - done defaults to False if not provided
    """
    global next_id
    new_task = {"id": next_id, "title": task_in.title, "done": task_in.done}
    tasks.append(new_task)
    next_id += 1
    return new_task


# ---------------------------------------------------------------------------
# PUT /tasks/{id}   (partial update)
# ---------------------------------------------------------------------------

@app.put("/tasks/{id}", response_model=Task, tags=["Tasks"])
def update_task(id: int, task_in: TaskUpdate):
    """
    Partially update an existing task.
    Only fields provided in the request body are changed.
    Returns 404 if the task does not exist.
    """
    for task in tasks:
        if task["id"] == id:
            if task_in.title is not None:
                task["title"] = task_in.title
            if task_in.done is not None:
                task["done"] = task_in.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {id} not found")


# ---------------------------------------------------------------------------
# DELETE /tasks/{id}
# ---------------------------------------------------------------------------

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(id: int):
    """Delete a task by id. Returns 204 on success, 404 if not found."""
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Task {id} not found")