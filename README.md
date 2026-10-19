# Tasks CRUD API with PostgreSQL and Docker

## About the Project

This project is a simple task management API built using FastAPI. Initially, the application used SQLite to store tasks. As part of this assignment, I updated it to use PostgreSQL and Docker so the database can run separately from the application and keep its data even when the containers are restarted.

The API allows users to create, view, update, and delete tasks.

## Technologies Used

- **Python and FastAPI** — to build the API
- **PostgreSQL** — to store task data
- **Psycopg** — to connect Python to PostgreSQL
- **Docker** — to run the application and database in containers
- **Docker Compose** — to start both services together

## Project Structure

- `main.py` — contains the API routes and request handling.
- `repository.py` — handles database operations such as creating, fetching, updating, and deleting tasks.
- `init.sql` — contains the SQL command to create the tasks table.
- `Dockerfile` — contains the instructions for building the application image.
- `docker-compose.yml` — configures and starts the application and PostgreSQL database.
- `.env` — stores local environment variables and database configuration.
- `.env.example` — provides an example of the required environment variables.
- `requirements.txt` — lists the Python packages needed to run the project.
- `.gitignore` — prevents files such as `.env` and Python cache files from being committed.

## How to Run the Project

### 1. Configure the environment

Create a `.env` file using `.env.example` as a reference. Add the required PostgreSQL password and database connection settings.

### 2. Start the application

Make sure Docker Desktop is running, then execute:

```bash
docker compose up --build -d
```

This builds the application image and starts the application and database containers.

### 3. Open the API documentation

Once the containers are running, visit:

http://localhost:8000/docs

You can use this page to test the available API endpoints.

## Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{task_id}` | Get a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{task_id}` | Update an existing task |
| DELETE | `/tasks/{task_id}` | Delete a task |

## Database Persistence

The PostgreSQL database uses a Docker volume to store its data outside the database container. This means the data can remain available even when the containers are stopped and recreated.

I tested this by creating a task, stopping the containers, starting them again, and checking the database. The task was still present after the restart.

## Stopping the Application

To stop the containers, run:

```bash
docker compose down
```

The database volume is kept, so the stored data remains available when the application is started again.

## Notes

Keep the `.env` file private and do not commit passwords or other sensitive configuration. Use `.env.example` when sharing the project so others know which environment variables they need to configure.

