# FastAPI Projects Monorepo

This repository contains two distinct FastAPI projects, demonstrating different aspects of building RESTful APIs with Python: a comprehensive Blog API and a User and Task Management API. Both projects leverage modern Python features, FastAPI's performance, and SQLAlchemy for database interactions, offering robust authentication and authorization mechanisms.

---

## Project 1: Blog API

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI Version](https://img.shields.io/badge/fastapi-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy Version](https://img.shields.io/badge/sqlalchemy-2.0.23-orange.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

### About the Blog API

This project is a RESTful Blog API built with FastAPI, designed to manage users, posts, comments, categories, and tags. It provides a full suite of CRUD (Create, Retrieve, Update, Delete) operations for blog content, complemented by robust JWT-based authentication and role-based authorization. Features like automatic slug generation for SEO-friendly URLs and interactive OpenAPI documentation are also included.

### Key Features

*   **User Management**: Secure user creation, retrieval, updates, and deletions with password hashing and roles (admin/regular).
*   **Content Management**: Comprehensive handling of blog posts, comments, categories, and tags.
*   **Authentication & Authorization**: JWT-based authentication and role-based access control for secure endpoints.
*   **SEO-Friendly URLs**: Automatic slug generation for posts and categories.
*   **Database**: Uses SQLite for ease of setup, configurable for other SQL databases.
*   **Interactive Documentation**: Self-generated Swagger UI and ReDoc documentation.

### Technologies Used

*   **FastAPI**: High-performance web framework.
*   **SQLAlchemy**: Python SQL toolkit and ORM.
*   **Pydantic**: Data validation.
*   **Passlib & python-jose**: For secure password hashing and JWT.
*   **python-dotenv**: Environment variable management.
*   **python-slugify**: For creating URL-friendly slugs.

### Getting Started

Refer to `blog.md` for detailed setup and installation instructions.

---

## Project 2: User and Task Management API

### About the User and Task Management API

This project implements a RESTful API using FastAPI for managing users and tasks. It focuses on demonstrating user registration, login with JWT authentication, fine-grained role-based access control (RBAC), and standard CRUD operations for both users and tasks, all built with asynchronous database interactions.

### Key Features

*   **User Authentication**: Register and login users securely with JWT tokens.
*   **Role-Based Access Control (RBAC)**: Restrict API access based on user roles (e.g., "admin", "user").
*   **User Management**: CRUD operations for users, with admin-only access for sensitive operations.
*   **Task Management**: CRUD operations for tasks, including filtering and admin-only creation/updates/deletions.
*   **Asynchronous Operations**: Utilizes `async/await` for efficient, non-blocking I/O.
*   **Database**: Uses SQLite for local development, with an asynchronous SQLAlchemy setup.
*   **Password Security**: Securely stores passwords using `bcrypt` via `passlib`.

### Technologies Used

*   **FastAPI**: Modern, asynchronous web framework.
*   **SQLAlchemy & aiosqlite**: Asynchronous ORM for SQLite.
*   **Pydantic**: Data validation and serialization.
*   **passlib & python-jose**: Password hashing and JWT handling.
*   **python-dotenv**: Environment variable management.
*   **uvicorn**: ASGI server for running the application.

### Getting Started

Refer to `to-do.md` for detailed setup and installation instructions.

---

## Overall Structure

This repository acts as a monorepo for these two independent FastAPI projects. Each project is designed to be runnable on its own and provides its own `README.md` (or equivalent documentation) with specific instructions.

### To run the Blog API:

1.  Navigate to the `blog-api` directory (if organized as such, or follow `blog.md`'s instructions directly).
2.  Follow the instructions in `blog.md`.

### To run the User and Task Management API:

1.  Navigate to the `user-task-api` directory (if organized as such, or follow `to-do.md`'s instructions directly).
2.  Follow the instructions in `to-do.md`.

---