# Event Management API

A backend REST API for managing events, users, authentication, and event ownership. Built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, **JWT authentication**, **Alembic**, **Google Gemini**, **Pytest**, and **Docker**.

## Overview

The Event Management API provides a structured backend for creating and managing events.

Authenticated users can create events and manage their own events, while the API provides filtering, pagination, validation, authentication, authorization, database migrations, AI-assisted descriptions, automated testing, and containerized deployment support.

## Features

* User registration and login
* JWT-based authentication
* Protected API endpoints
* User-based event ownership
* Event CRUD operations
* Partial event updates using PATCH
* Request and response validation with Pydantic
* Event filtering by location
* Pagination using `skip` and `limit`
* PostgreSQL database integration
* SQLAlchemy ORM
* Alembic database migrations
* AI-assisted event description generation
* Pytest API testing
* Docker containerization
* Docker Compose with PostgreSQL
* Interactive API documentation with Swagger UI

## Tech Stack

| Technology     | Purpose                            |
| -------------- | ---------------------------------- |
| Python         | Backend programming                |
| FastAPI        | REST API framework                 |
| Pydantic       | Data validation and schemas        |
| SQLAlchemy     | ORM and database interaction       |
| PostgreSQL     | Relational database                |
| JWT            | Authentication                     |
| Alembic        | Database migrations                |
| Google Gemini  | AI-assisted description generation |
| Pytest         | Automated API testing              |
| Docker         | Containerization                   |
| Docker Compose | API + database orchestration       |

## Project Structure

```text
Event-Management-API/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── services/
│   └── ai_services.py
│
├── tests/
│   └── test_basic.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── database.py
├── main.py
├── models.py
├── requirements.txt
├── schemas.py
└── security.py
```

## API Endpoints

### Authentication

| Method | Endpoint    | Description                        |
| ------ | ----------- | ---------------------------------- |
| POST   | `/register` | Register a new user                |
| POST   | `/login`    | Authenticate user and generate JWT |

### Events

| Method | Endpoint             | Description                              |
| ------ | -------------------- | ---------------------------------------- |
| POST   | `/events`            | Create an event                          |
| GET    | `/events`            | Get events with filtering and pagination |
| GET    | `/events/{event_id}` | Get a specific event                     |
| PATCH  | `/events/{event_id}` | Partially update an event                |
| DELETE | `/events/{event_id}` | Delete an event                          |

### AI

| Method | Endpoint                   | Description                            |
| ------ | -------------------------- | -------------------------------------- |
| POST   | `/ai/generate-description` | Generate an event description using AI |

## Authentication

The API uses **JSON Web Tokens (JWT)** for authentication.

After successful login, the API returns an access token. Protected endpoints require the token in the request header:

```text
Authorization: Bearer <access_token>
```

JWT authentication is also used to identify the current user and enforce event ownership.

## Event Ownership

Each event is associated with the user who created it.

This relationship is represented using a foreign key:

```text
users.id
   ↓
events.user_id
```

Users can update or delete only events that they own.

Unauthorized access attempts return an appropriate HTTP error response.

## Filtering & Pagination

The events endpoint supports filtering and pagination.

Example:

```text
GET /events?location=Chennai&skip=0&limit=10
```

Parameters:

* `location` — Filter events by location
* `skip` — Number of records to skip
* `limit` — Maximum number of records to return

## AI Integration

The project integrates Google Gemini to generate event descriptions.

If an event is created without a description, the backend can generate one using the AI service.

The AI functionality is implemented separately in:

```text
services/ai_services.py
```

## Database

The application uses **PostgreSQL** with **SQLAlchemy ORM**.

Main database tables:

```text
users
events
```

The `events` table contains a foreign key referencing the `users` table to maintain event ownership.

## Database Migrations

**Alembic** is used to manage database schema changes.

Apply the latest migration:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@db:5432/Event
SECRET_KEY=your_secret_key
GEMINI_API_KEY=your_gemini_api_key
```

> Never commit your real `.env` file or API keys to GitHub.

A safe `.env.example` file is included in the repository.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/aysha-nasrin26/Event-Management-API.git
cd Event-Management-API
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

### 5. Run database migrations

```powershell
alembic upgrade head
```

### 6. Start the API

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Docker Setup

The project includes Docker configuration for running the API and PostgreSQL together.

Start the services:

```powershell
docker compose up --build
```

The API will be available at:

```text
http://localhost:8001
```

Swagger documentation:

```text
http://localhost:8001/docs
```

Stop the services:

```powershell
docker compose down
```

## API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
/docs
```

### ReDoc

```text
/redoc
```

When the application is running locally:

```text
http://127.0.0.1:8000/docs
```

## Testing

The project uses **Pytest** for API testing.

Run:

```powershell
pytest
```

The test suite covers areas such as:

* Event creation
* Event retrieval
* Event updates
* Event deletion
* Authentication
* Unauthorized requests
* Invalid event IDs
* Event ownership authorization

## Security

Security-related practices implemented in the project include:

* JWT-based authentication
* Protected endpoints
* Password hashing
* User-based authorization
* Environment variables for secrets
* `.gitignore` protection for `.env`
* No API keys committed to the repository

## Future Improvements

Potential future improvements include:

* Production deployment
* Refresh tokens
* Role-based access control
* Email notifications
* Event registration and attendee management
* Advanced search and filtering
* CI/CD integration
* Production monitoring and logging

## Author

**Aysha Nasrin**

BCA Graduate | Gold Medalist | Python & Backend Developer

GitHub:
https://github.com/aysha-nasrin26

Portfolio:
https://ayshanasrin.dev/

---

⭐ If you find this project useful, feel free to explore the repository.
