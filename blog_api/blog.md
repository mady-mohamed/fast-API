# Blog API

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI Version](https://img.shields.io/badge/fastapi-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-2.0.23-orange.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Admin Privileges](#admin-privileges)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## About

This project is a RESTful Blog API built with FastAPI, designed to manage users, posts, comments, categories, and tags. It provides endpoints for creating, retrieving, updating, and deleting blog content, with robust authentication and authorization features.

## Features

- **User Management**: Create, retrieve, update, and delete users. Includes password hashing and user roles (admin/regular).
- **Post Management**: Create, retrieve, update, and delete blog posts. Supports post status (draft/published), categories, and tags.
- **Comment Management**: Create, retrieve, update, and delete comments on posts.
- **Category Management**: Create, retrieve, update, and delete categories for posts.
- **Tag Management**: Create, retrieve, update, and delete tags for posts.
- **Authentication**: JWT-based authentication for securing API endpoints.
- **Authorization**: Role-based access control (Admin vs. User) for specific operations.
- **Slug Generation**: Automatic slug generation for posts and categories for SEO-friendly URLs.
- **Database**: SQLite for simplicity, easily configurable for other SQL databases.
- **Interactive Documentation**: Self-generated OpenAPI (Swagger UI) documentation.

## Technologies Used

- **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **SQLAlchemy**: Python SQL toolkit and Object Relational Mapper (ORM) that gives application developers the full power and flexibility of SQL.
- **Pydantic**: Data validation and settings management using Python type hints.
- **Passlib**: Cryptography library for secure password hashing.
- **python-jose**: JWT (JSON Web Token) implementation in Python.
- **python-dotenv**: Reads key-value pairs from a `.env` file and sets them as environment variables.
- **python-slugify**: A Python slugify application that can slugify Unicode strings.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- `pip` (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/blog-api.git
    cd blog-api
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` yet, you can create one from your current environment:
    ```bash
    pip install "fastapi[all]" sqlalchemy pydantic python-jose python-dotenv passlib python-slugify uvicorn
    pip freeze > requirements.txt
    ```

### Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```dotenv
SECRET_KEY="your-super-secret-key-change-this-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

-   `SECRET_KEY`: A strong, random string used for signing JWT tokens. **Change this for production!**
-   `ALGORITHM`: The algorithm used for JWT encoding (e.g., `HS256`).
-   `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for access tokens in minutes.

### Running the Application

Once everything is installed and configured, you can run the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reloading when code changes are detected, which is great for development.

The API will be accessible at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation.
You can access it at:

-   **Swagger UI**: `http://127.0.0.1:8000/docs` 
-   **ReDoc**: `http://127.0.0.1:8000/redoc` 

## Authentication

This API uses JWT (JSON Web Token) for authentication.

1.  **Register a user**: Use the `/users/` endpoint to create a new user.
2.  **Login**: Send a `POST` request to `/login` with `username` and `password` as `x-www-form-urlencoded` data. You will receive an `access_token` in return.
3.  **Authorize**: Include the `access_token` in the `Authorization` header of subsequent requests as a Bearer token (e.g., `Authorization: Bearer <your_access_token>`).

## Admin Privileges

Some endpoints are restricted to admin users only. An admin user is identified by the `is_admin` field in the `User` model being `True`. The `create_user` endpoint, for example, initially requires an admin user to perform the creation.

You can set a user to be an admin by updating their `is_admin` field (e.g., via the `/users/{username}` PUT endpoint, but this would require an existing admin or direct database manipulation to set up the first admin).

## Project Structure

-   `main.py`: The main FastAPI application, defining all API endpoints.
-   `crud.py`: Contains functions for interacting with the database (Create, Read, Update, Delete operations).
-   `models.py`: Defines the SQLAlchemy ORM models for the database tables (User, Post, Comment, Category, Tag).
-   `schemas.py`: Defines Pydantic models for request and response data validation.
-   `auth.py`: Handles authentication logic, including password hashing, JWT creation/verification, and dependency for current user/admin checks.
-   `database.py`: Configures the database connection and provides a dependency for database sessions.
-   `.env`: Environment variables configuration file.
-   `requirements.txt`: Lists Python dependencies.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.