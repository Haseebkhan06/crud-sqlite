
from pathlib import Path
import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

DATABASE = Path(__file__).with_name("tasks.db")
app = FastAPI()


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        if count == 0:
            example_tasks = [
                ("Learn Python", 0),
                ("Build a CRUD API", 0),
                ("Connect SQLite database", 0),
            ]

            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                example_tasks,
            )

        conn.commit()
    finally:
        conn.close()


init_db()


@app.get("/tasks")
def get_tasks():
    conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }
            for row in rows
        ]
    finally:
        conn.close()


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"},
            )

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }
    finally:
        conn.close()


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

    conn = get_connection()

    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            (title, 0),
        )
        conn.commit()

        return {
            "id": cursor.lastrowid,
            "title": title,
            "done": False,
        }
    finally:
        conn.close()


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"},
            )

        title = row["title"]
        done = bool(row["done"])

        if task.title is not None:
            if not task.title.strip():
                return JSONResponse(
                    status_code=400,
                    content={"error": "Title is required"},
                )
            title = task.title.strip()

        if task.done is not None:
            done = task.done

        conn.execute(
            "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
            (title, int(done), task_id),
        )
        conn.commit()

        return {
            "id": task_id,
            "title": title,
            "done": done,
        }
    finally:
        conn.close()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_connection()

    try:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )
        conn.commit()

        if cursor.rowcount == 0:
            return JSONResponse(
                status_code=404,
                content={"error": "Task not found"},
            )

        return {
            "message": "Task deleted successfully",
            "id": task_id,
        }
    finally:
        conn.close()
