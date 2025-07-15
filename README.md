# Mini Social Network API

A simple social network API built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **Authentication**: User registration and JWT-based login.
- **Users**: View user profiles, follow, and unfollow.
- **Posts**: Create, view, edit, and delete posts.
- **Likes**: Like and unlike posts.

## Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- JWT Authentication
- Docker & Docker Compose

## Project Structure

```
app/
├── api/
│   ├── deps.py
│   └── v1/
│       └── routers/
│           ├── auth.py
│           ├── users.py
│           ├── posts.py
│           └── likes.py
│       └── schemas/
├── core/
├── models/
├── services/
└── main.py
```

## Setup and Running

### 1. Environment Variables

Copy the example `.env.example` file to `.env` and fill in your database and security details.

```bash
cp .env.example .env
```

### 2. Run with Docker (Recommended)

Build and run the containers using Docker Compose:

```bash
docker-compose up --build
```

### 3. Run Locally

1.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Documentation

Once the application is running, you can access the API documentation at:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) 