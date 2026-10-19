
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/tasks")
def get_tasks():
    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": row["done"],
        }
        for row in repository.get_tasks()
    ]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    row = repository.get_task(task_id)

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": row["done"],
    }


class TaskCreate(BaseModel):
    title: str


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()

    if not title:
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required"},
        )

    return repository.create_task(title)


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    row = repository.get_task(task_id)

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    title = row["title"]
    done = row["done"]

    if task.title is not None:
        if not task.title.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Title is required"},
            )
        title = task.title.strip()

    if task.done is not None:
        done = task.done

    return repository.update_task(task_id, title, done)


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    row = repository.delete_task(task_id)

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"},
        )

    return {
        "message": "Task deleted successfully",
        "id": row["id"],
    }
