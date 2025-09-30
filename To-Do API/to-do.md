
# FastAPI Project: User and Task Management

This project implements a RESTful API using FastAPI for managing users and tasks. It includes features like user registration, login with JWT authentication, role-based access control, and CRUD operations for both users and tasks.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Installation Steps](#installation-steps)
- [Database](#database)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [User Management](#user-management)
  - [Task Management](#task-management)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication:** Register, login, and authenticate users using JWT tokens.
- **Role-Based Access Control (RBAC):** Restrict access to certain endpoints based on user roles (e.g., "admin", "user").
- **User Management:**
    - Create new users (registration).
    - Retrieve user information (admin only).
    - Update user details (admin only).
    - Delete users (admin only).
- **Task Management:**
    - Create tasks (admin only).
    - Retrieve tasks (all authenticated users).
    - Update tasks (admin only).
    - Delete tasks (admin only).
- **Asynchronous Operations:** Utilizes `async/await` for non-blocking I/O with the database.
- **SQLite Database:** Uses SQLite for local development and testing.
- **Password Hashing:** Securely stores user passwords using `bcrypt`.

## Project Structure

```
.
├── main.py
├── db.py
├── password.py
├── schemas.py
├── .env
├── test.db (generated after first run)
└── README.md
```

- **`main.py`**: The main FastAPI application file, defining all the API endpoints.
- **`db.py`**: Contains the database schema definition using SQLAlchemy and asynchronous CRUD operations for users and tasks.
- **`password.py`**: Handles password hashing, JWT token creation/decoding, and authentication dependencies.
- **`schemas.py`**: Defines Pydantic models for request and response data validation.
- **`.env`**: Stores environment variables like `SECRET_KEY` and `ACCESS_TOKEN_EXPIRE_MINUTES`.
- **`test.db`**: The SQLite database file, automatically created on the first run if it doesn't exist.

## Setup and Installation

### Prerequisites

- Python 3.7+
- `pip` (Python package installer)

### Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```ini
SECRET_KEY="your-super-secret-key-replace-this-with-a-strong-random-string"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- **`SECRET_KEY`**: A strong, random string used for signing JWT tokens. **Change this to a secure, unique value.**
- **`ALGORITHM`**: The cryptographic algorithm used for JWT. `HS256` is a common choice.
- **`ACCESS_TOKEN_EXPIRE_MINUTES`**: The duration in minutes for which an access token remains valid.

### Installation Steps

1. **Clone the repository (if applicable) or create the project files.**
2. **Navigate to the project directory:**
   ```bash
   cd your-project-name
   ```
3. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install the required dependencies:**
   ```bash
   pip install "fastapi[all]" uvicorn sqlalchemy aiosqlite python-dotenv passlib "python-jose[cryptography]"
   ```
   This command installs:
   - `fastapi`: The web framework.
   - `uvicorn`: An ASGI server for running FastAPI.
   - `sqlalchemy`: SQL toolkit and Object-Relational Mapper (ORM).
   - `aiosqlite`: Asynchronous SQLite driver for SQLAlchemy.
   - `python-dotenv`: For loading environment variables.
   - `passlib`: For password hashing.
   - `python-jose[cryptography]`: For JWT token handling.

## Database

The project uses `SQLite` as the database. The database file `test.db` will be created automatically in the project root directory the first time the application runs if it doesn't already exist.

**`db.py`**
- Defines two tables: `user_table` and `task_table`.
- Provides asynchronous functions for:
    - `create_tables()`: Initializes the database schema.
    - `insert_user()`, `get_users()`, `update_user()`, `delete_user()` for user management.
    - `insert_task()`, `get_task()`, `get_tasks()`, `update_task()`, `delete_task()` for task management.

## API Endpoints

All endpoints are served by the FastAPI application.

### Authentication

- **`POST /register`**
  - **Description:** Registers a new user.
  - **Request Body:** `User` schema (username, password, optional role).
  - **Response:** `{"message": "User created"}`
  - **Example:**
    ```json
    {
      "username": "testuser",
      "password": "password123",
      "role": "user"
    }
    ```

- **`POST /login`**
  - **Description:** Authenticates a user and returns an access token.
  - **Request Body:** OAuth2 password request form data (username, password).
  - **Response:** `{"access_token": "...", "token_type": "bearer"}`
  - **Example (Form Data):**
    ```
    username: testuser
    password: password123
    ```

- **`GET /me`**
  - **Description:** Retrieves information about the current authenticated user.
  - **Requires:** Valid JWT token (in Authorization header or `token` query parameter).
  - **Response:** `UserProfile` schema (username, role).

- **`GET /protected`**
  - **Description:** An example protected route, accessible only to authenticated users with any role.
  - **Requires:** Valid JWT token.
  - **Response:** `{"message": "Hello, {username}. You are authorized!"}`

- **`GET /admin_only`**
  - **Description:** An example protected route, accessible only to authenticated users with the "admin" role.
  - **Requires:** Valid JWT token with "admin" role.
  - **Response:** `{"message": "Welcome Admin {username}"}`

### User Management (Admin Only)

These endpoints require an "admin" role.

- **`GET /db_users`**
  - **Description:** Retrieves a list of all users.
  - **Requires:** Valid JWT token with "admin" role.
  - **Response:** List of user dictionaries.

- **`GET /user`**
  - **Description:** Retrieves a single user by ID.
  - **Requires:** Valid JWT token with "admin" role.
  - **Query Parameters:** `id: int`
  - **Response:** User dictionary.

- **`PUT /users/{user_id}`**
  - **Description:** Updates a user's role, name, or password.
  - **Requires:** Valid JWT token with "admin" role.
  - **Path Parameters:** `user_id: int`
  - **Request Body:** `UserUpdate` schema (optional role, name, password).
  - **Response:** `{"message": "User updated"}`

- **`DELETE /users/{user_id}`**
  - **Description:** Deletes a user by ID.
  - **Requires:** Valid JWT token with "admin" role.
  - **Path Parameters:** `user_id: int`
  - **Response:** `{"message": "User deleted"}`

### Task Management

- **`GET /tasks/{task_id}`**
  - **Description:** Retrieves a single task by ID.
  - **Requires:** Valid JWT token (any role).
  - **Path Parameters:** `task_id: int`
  - **Response:** `Task` schema.

- **`GET /tasks`**
  - **Description:** Retrieves a list of tasks, with optional filtering by name, sprint, or progress.
  - **Requires:** Valid JWT token (any role).
  - **Query Parameters:**
    - `name: str` (optional)
    - `sprint: int` (optional)
    - `progress: str` (optional, accepts "todo", "in-progress", "done")
  - **Response:** List of `Task` schemas.

- **`POST /tasks`**
  - **Description:** Creates a new task.
  - **Requires:** Valid JWT token with "admin" role.
  - **Request Body:** `Task` schema (name, progress, sprint, optional start_date).
  - **Response:** `{"message": "Task created"}`

- **`PUT /tasks/{task_id}`**
  - **Description:** Updates an existing task.
  - **Requires:** Valid JWT token with "admin" role.
  - **Path Parameters:** `task_id: int`
  - **Request Body:** `Task` schema (name, progress, sprint, optional start_date).
  - **Response:** Updated `Task` schema.

- **`DELETE /tasks/{task_id}`**
  - **Description:** Deletes a task by ID.
  - **Requires:** Valid JWT token with "admin" role.
  - **Path Parameters:** `task_id: int`
  - **Response:** No content on success.

## Running the Application

1. **Start the FastAPI application using Uvicorn:**
   ```bash
   uvicorn main:app --reload
   ```
   The `--reload` flag enables auto-reloading of the server when code changes are detected, which is useful for development.

2. **Access the API Documentation:**
   Once the server is running, you can access the interactive API documentation (Swagger UI) at:
   - `http://127.0.0.1:8000/docs`
   - Or, the ReDoc documentation at `http://127.0.0.1:8000/redoc`

   This documentation allows you to explore the endpoints, their parameters, and even test them directly from your browser.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests.

## License

This project is open-source and available under the MIT License.